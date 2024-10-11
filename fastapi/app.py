from typing import Union, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from database import *
from routes.users import router
from starlette.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
app = FastAPI()


# Include the router for user-related routes with "/api" prefix
app.include_router(router, prefix="/api")

# Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection handling
connected_clients: List[WebSocket] = []

@app.websocket("/ws/game_stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data length: {len(data)}")  # Debug message
            # Broadcast the data to all connected clients
            for client in connected_clients:
                if client != websocket and client.application_state == WebSocketState.CONNECTED:
                    await client.send_text(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"Error: {e}")

# Database connection handling
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# Define Pydantic model to validate incoming data
class GameStatModel(BaseModel):
    quantitys: int
    time_spent: int
    target1: Optional[int] = None  # Default to None if not provided
    target2: Optional[int] = None
    Robot1C: int
    Robot1P: int
    Robot2C: int
    Robot2P: int
    Robot3C: int
    Robot3P: int
    Robot4C: int
    Robot4P: int
    Robot5C: int
    Robot5P: int
    Robot6C: int
    Robot6P: int
    Robot7C: int
    Robot7P: int
    Robot8C: int
    Robot8P: int
    Robot9C: int
    Robot9P: int
    Robot10C: int
    Robot10P: int

# Submit game stats API route
@app.post("/submit_game_stats")
async def submit_game_stats(variable: GameStatModel):
    try:
        # Get the next experiment number (exp_number should be the same across game_stat, robot_stat, robot_rank)
        exp_number = await get_next_experiment_number()

        # Insert game stats into the game_stat table
        await insert_game_stat(
            objectamount=variable.quantitys,
            pygametime=variable.time_spent,
            target1=variable.target1,
            target2=variable.target2
        )

        # Insert robot stats for 10 robots into the robot_stat table (using the same exp_number for all)
        robot_stats = []
        for i in range(1, 11):
            robot_stats.append({
                "robot_id": i,
                "robottime": getattr(variable, f"Robot{i}C"),
                "robotpath": getattr(variable, f"Robot{i}P")
            })
        # Insert robot stats for all 10 robots using the same exp_number
        await insert_robot_stat(exp_number=exp_number, robots=robot_stats)

        # Insert top 3 robots into the robot_rank table (based on collected boxes)
        top_3_robots = sorted(robot_stats, key=lambda x: x['robottime'], reverse=True)[:3]
        await insert_robot_rank(exp_number=exp_number, robots=top_3_robots)

        return {"message": "Game stats submitted successfully"}

    except Exception as e:
        print(f"Error: {e}")  # Log the error to console for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")

