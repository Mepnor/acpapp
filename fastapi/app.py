# app.py
from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from database import *
from routes.users import router
from starlette.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")
# Include the router for user-related routes with "/api" prefix
app.include_router(router, prefix="/api")

# Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if your frontend runs on a different port
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
    time_when_end: int
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

class TopPerformanceModel(BaseModel):
    robot_id: int
    ranking: int
    rtype: str
    robottime: int
    robotpath: int

class GameStatsPayload(BaseModel):
    gameStats: GameStatModel  # Existing game stats structure
    topPerformance: List[TopPerformanceModel] # List of top 6 performances

# Submit game stats API route with "/api" prefix
@app.post("/api/submit_game_stats")
async def submit_game_stats(payload: GameStatsPayload):
    try:
        # Start a transaction to ensure all operations happen atomically
        async with database.transaction():
            # Step 1: Insert into the game_stat table and get the exp_number
            game_stat = await insert_game_stat(
                objectamount=payload.gameStats.quantitys,
                pygametime=payload.gameStats.time_spent,
                timetofinish=payload.gameStats.time_when_end,
                target1=payload.gameStats.target1,
                target2=payload.gameStats.target2,
            )
            exp_number = game_stat["exp_number"]  # Retrieve the correct exp_number

            # Step 2: Insert robot stats for all 10 robots with the correct exp_number
            robot_stats = [
                {
                    "robot_id": i + 1,
                    "robottime": getattr(payload.gameStats, f"Robot{i + 1}C"),
                    "robotpath": getattr(payload.gameStats, f"Robot{i + 1}P"),
                }
                for i in range(10)
            ]
            await insert_robot_stat(exp_number=exp_number, robots=robot_stats)

            # Step 3: Get the top 3 robots for "Box Collected"
            top_3_boxes = sorted(robot_stats, key=lambda x: x["robottime"], reverse=True)[:3]
            for rank, robot in enumerate(top_3_boxes, start=1):
                robot["ranking"] = rank
                robot["rtype"] = "Box Collected"

            # Step 4: Get the top 3 robots for "Longest Distance"
            top_3_distances = sorted(robot_stats, key=lambda x: x["robotpath"], reverse=True)

            # Filter out robots that are already in top_3_boxes to avoid duplicates
            top_3_distances = [robot for robot in top_3_distances if robot["robot_id"] not in [r["robot_id"] for r in top_3_boxes]][:3]

            for rank, robot in enumerate(top_3_distances, start=1):
                robot["ranking"] = rank
                robot["rtype"] = "Longest Distance"

            # Step 5: Create a combined list to insert in the desired order
            top_performance = top_3_boxes + top_3_distances

            # Step 6: Insert the top performances into the robot_rank table
            await insert_robot_rank(exp_number=exp_number, robots=top_performance)

        return {"message": "Game stats and top performances submitted successfully"}

    except Exception as e:
        print(f"Error: {e}")  # Print the error for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")
