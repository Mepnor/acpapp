from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from database import (
    get_user_by_FactoryID,
    get_user_by_gmail,
    insert_user,
    get_user,
    update_user,
    delete_user,
    get_game_stat,
    delete_game_stat_and_related,
    store_token,
    authenticate_user
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
import logging

SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/LoginWithToken")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gmail: Optional[str]
    dob: Optional[str]

# Pydantic models
class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    created_at: datetime

class UserLogin(BaseModel):
    factory_id: str
    password: str

class StoreToken(BaseModel):
    token: str
    user_id: int


class GetGameStat(BaseModel):
    exp_number: int
    objectamount: int
    pygametime: int
    timetofinish: int
    target1: int
    target2: int
    timestamp: datetime
class UpdateUserProfile(BaseModel):
    first_name: str
    last_name: str
    gmail: str
    dob: str
    avatar_url: Optional[str] = None

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    password: str
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    factory_id: str
    gmail: str
    dob: str
    created_at: datetime

    class Config:
        orm_mode = True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# Define get_current_user function
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user(user_id)
    if user is None:
        raise credentials_exception
    return user


# Endpoint to get current user
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
# Endpoint to get user's avatar
# Endpoint to get user's avatar
@router.get("/users/me/avatar")
async def get_user_avatar(current_user: User = Depends(get_current_user)):
    user = await get_user(current_user.user_id)
    if user and user['avatar']:
        return Response(content=user['avatar'], media_type="image/jpeg")
    else:
        # Return a default image or 404
        raise HTTPException(status_code=404, detail="Avatar not found")
    
# Endpoint to get a user by user_id
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    result = await get_user(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/users/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    print(f"Received user data: {user}")
    
    existing_factory = await get_user_by_FactoryID(user.factory_id)
    if existing_factory:
        raise HTTPException(status_code=400, detail="Factory ID already registered")

    existing_gmail = await get_user_by_gmail(user.gmail)
    if existing_gmail:
        raise HTTPException(status_code=400, detail="Gmail already registered")

    # Insert the new user into the database
    result = await insert_user(
        user.first_name,
        user.last_name,
        user.factory_id,
        user.gmail,
        user.dob,
        get_password_hash(user.password)  # Hash the password
    )

    if result is None:
        raise HTTPException(status_code=400, detail="Error creating user")

    # Return the response without the password
    return UserResponse(
        user_id=result["user_id"],
        first_name=result["first_name"],
        last_name=result["last_name"],
        factory_id=result["factory_id"],
        gmail=result["gmail"],
        dob=result["dob"],
        created_at=result["created_at"]
    )
# Make sure this route is placed **after** `/users/create`
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    result = await get_user(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.put("/users/update", response_model=User)
async def update_user_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    gmail: str = Form(...),
    dob: str = Form(...),
    old_password: Optional[str] = Form(None),
    new_password: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
):
    # Verify old password before allowing new password to be set
    if old_password and new_password:
        if not verify_password(old_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        hashed_new_password = get_password_hash(new_password)
    else:
        hashed_new_password = current_user.password_hash  # Keep the same password if no new password is provided

    # Update the user profile
    updated_user = await update_user(
        user_id=current_user.user_id,
        first_name=first_name,
        last_name=last_name,
        gmail=gmail,
        dob=dob,
        password_hash=hashed_new_password
    )
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Error updating user")
    return updated_user


# Endpoint to delete a user by user_id (if needed)
@router.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int):
    result = await delete_user(user_id)
    
    if result is None:  # Handle case where no matching user was found.
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": f"User with ID {user_id} deleted successfully"}

# Endpoint for user login to get JWT token

@router.post("/users/LoginWithToken")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Check if factory_id or password is missing
        if not form_data.username:
            raise HTTPException(status_code=400, detail="Please input factory ID")
        
        if not form_data.password:
            raise HTTPException(status_code=400, detail="Please input a password")

        # Authenticate user
        db_user = await authenticate_user(factory_id=form_data.username, password=form_data.password)
        if db_user is None:
            raise HTTPException(status_code=401, detail="Incorrect Factory ID or password")

        # Generate the access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": db_user["user_id"]}, expires_delta=access_token_expires
        )

        # Store the token in the database
        await store_token(user_id=db_user["user_id"], token=access_token)

        # Return the token
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as e:
        raise e  # Raise the error properly

    except Exception as e:
        print(f"Error in login_for_access_token: {str(e)}")  # Log for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")



# Optional: Endpoint for user login (if needed)
@router.post("/users/login")
async def login_user(user: UserLogin):
    db_user = await get_user_by_FactoryID(user.factory_id)
    if db_user is None or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Factory ID or password")

    # Optionally, create a JWT token here if not using /users/token
    # ...

    return User(
        user_id=db_user.user_id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        factory_id=db_user.factory_id,
        gmail=db_user.gmail,
        dob=db_user.dob,
        created_at=db_user.created_at
    )

# Other endpoints
@router.get("/game_stat/{exp_number}", response_model=GetGameStat)
async def read_game_stat(exp_number: int):
    result = await get_game_stat(exp_number)
    if result is None:
        raise HTTPException(status_code=404, detail="Experiment id not found.")
    return result

@router.delete("/all_stat/{exp_number}")
async def delete_experiment(exp_number: int):
    result = await delete_game_stat_and_related(exp_number)
    if result is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return {"detail": f"Data with Experiment Number {exp_number} deleted successfully"}