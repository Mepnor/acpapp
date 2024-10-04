from databases import Database

POSTGRES_USER = "temp"
POSTGRES_PASSWORD = "temp"
POSTGRES_DB = "advcompro"
POSTGRES_HOST = "db"

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

database = Database(DATABASE_URL)

async def connect_db():
    await database.connect()
    print("Database connected")

async def disconnect_db():
    await database.disconnect()
    print("Database disconnected")



# Function to insert a new user into the users table
async def insert_user(first_name: str, last_name: str, factory_id: str, gmail: str, dob: str, password_hash: str):
    query = """
    INSERT INTO pnor (first_name, last_name, factory_id, gmail, dob, password_hash)
    VALUES (:first_name, :last_name, :factory_id, :gmail, :dob, :password_hash)
    RETURNING user_id, first_name, last_name, factory_id, gmail, dob, password_hash, created_at
    """
    values = {
        "first_name": first_name,
        "last_name": last_name,
        "factory_id": factory_id,
        "gmail": gmail,
        "dob": dob,
        "password_hash": password_hash
    }
    return await database.fetch_one(query=query, values=values)


# Function to select a user by user_id from the users table
async def get_user(user_id: int):
    query = "SELECT * FROM pnor WHERE user_id = :user_id"
    return await database.fetch_one(query=query, values={"user_id": user_id})

async def get_user_by_gmail(gmail: str):
   query = "SELECT * FROM pnor WHERE gmail = :gmail"
   return await database.fetch_one(query=query, values={"gmail": gmail})

async def get_user_by_FactoryID(factory_id: str):
   query = "SELECT * FROM pnor WHERE factory_id = :factory_id"
   return await database.fetch_one(query=query, values={"factory_id": factory_id})
# Function to update a user in the users table
async def update_user(user_id: int, first_name: str, password_hash: str, gmail: str):
    query = """
    UPDATE pnor 
    SET first_name = :first_name, password_hash = :password_hash, gmail = :gmail
    WHERE user_id = :user_id
    RETURNING user_id, first_name, password_hash, gmail, created_at
    """
    values = {"user_id": user_id, "first_name": first_name, "password_hash": password_hash, "gmail": gmail}
    return await database.fetch_one(query=query, values=values)

# Function to delete a user from the users table
async def delete_user(user_id: int):
    query = "DELETE FROM pnor WHERE user_id = :user_id RETURNING *"
    return await database.fetch_one(query=query, values={"user_id": user_id})


