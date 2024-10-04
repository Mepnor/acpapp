from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import *  # Ensure your database functions are imported

router = APIRouter()

# Pydantic model for user creation
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    password_hash: str

# Pydantic model for user update
class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    factory_id: Optional[str]
    gmail: Optional[str]
    dob: Optional[str]
    password_hash: Optional[str]

# Pydantic model for user response
class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    created_at: datetime

# Pydantic model for login
class UserLogin(BaseModel):
    factory_id: str
    password_hash: str

# Endpoint to create a new user
@router.post("/users/create", response_model=User)
async def create_user(user: UserCreate):
    # Check if the factory_id already exists
    existing_factory = await get_user_by_FactoryID(user.factory_id)
    if existing_factory:
        raise HTTPException(status_code=400, detail="Factory ID already registered")
    
    # Check if the email (gmail) already exists
    existing_gmail = await get_user_by_gmail(user.gmail)
    if existing_gmail:
        raise HTTPException(status_code=400, detail="Gmail already registered")

    # Insert the new user into the database
    result = await insert_user(
        user.first_name, user.last_name, user.factory_id, user.gmail, user.dob, user.password_hash
    )

    if result is None:
        raise HTTPException(status_code=400, detail="Error creating user")

    # Format the response based on the User model
    return User(
        user_id=result["user_id"],
        first_name=user.first_name,
        last_name=user.last_name,
        factory_id=user.factory_id,
        gmail=user.gmail,
        dob=user.dob,
        created_at=datetime.now()  # Update to reflect actual DB insertion time if available
    )


# Endpoint to get a user by user_id
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    result = await get_user(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

# Endpoint to update a user by user_id
@router.put("/users/{user_id}", response_model=User)
async def update_user_endpoint(user_id: int, user: UserUpdate):
    existing_user = await get_user(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    result = await update_user(
        user_id=user_id,
        first_name=user.first_name or existing_user['first_name'],
        last_name=user.last_name or existing_user['last_name'],
        factory_id=user.factory_id or existing_user['factory_id'],
        gmail=user.gmail or existing_user['gmail'],
        dob=user.dob or existing_user['dob'],
        password_hash=user.password_hash or existing_user['password_hash']
    )
    
    if result is None:
        raise HTTPException(status_code=400, detail="Error updating user")
    return result

# Endpoint to delete a user by user_id (if needed)
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    result = await delete_user(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

# Endpoint for user login
@router.post("/users/login")
async def login_user(user: UserLogin):
    db_user = await get_user_by_FactoryID(user.factory_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid Factory ID or password")

    return User(
        user_id=db_user.user_id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        factory_id=db_user.factory_id,
        gmail=db_user.gmail,
        dob=db_user.dob,
        created_at=db_user.created_at
    )
