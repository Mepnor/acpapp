from databases import Database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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




async def insert_user(first_name: str, last_name: str, factory_id: str, gmail: str, dob: str, password_hash: str):
    query = """
    INSERT INTO pnor (first_name, last_name, factory_id, gmail, dob, password_hash)
    VALUES (:first_name, :last_name, :factory_id, :gmail, :dob, :password_hash)
    RETURNING user_id, first_name, last_name, factory_id, gmail, dob, created_at
    """
    values = {
        "first_name": first_name,
        "last_name": last_name,
        "factory_id": factory_id,
        "gmail": gmail,
        "dob": dob,
        "password_hash": password_hash,
    }
    return await database.fetch_one(query=query, values=values)

async def insert_login(factory_id: str, password_hash: str):
    query = """
    INSERT INTO pnor_login (factory_id, password_hash)
    VALUES (:factory_id, :password_hash)
    RETURNING login_log, factory_id, password_hash, login_time
    """
    values = {
        "factory_id": factory_id,
        "password_hash": password_hash,
    }
    return await database.fetch_one(query=query, values=values)
# Function to select a user by user_id from the users table
async def get_user(user_id: int):
    query = "SELECT * FROM pnor WHERE user_id = :user_id"
    return await database.fetch_one(query=query, values={"user_id": user_id})

# Function to get a user by gmail
async def get_user_by_gmail(gmail: str):
   query = "SELECT * FROM pnor WHERE gmail = :gmail"
   return await database.fetch_one(query=query, values={"gmail": gmail})

# Function to get a user by Factory ID
async def get_user_by_FactoryID(factory_id: str):
   query = "SELECT * FROM pnor WHERE factory_id = :factory_id"
   return await database.fetch_one(query=query, values={"factory_id": factory_id})

async def get_user_by_FactoryID_Login(factory_id: str):
   query = "SELECT * FROM pnor_login WHERE factory_id = :factory_id"
   return await database.fetch_one(query=query, values={"factory_id": factory_id})

# Function to update a user in the pnor table
async def update_user(
    user_id: int,
    first_name: str = None,
    last_name: str = None,
    gmail: str = None,
    dob: str = None,
    password_hash: str = None,
):
    query = "UPDATE pnor SET "
    values = {"user_id": user_id}
    updates = []

    if first_name is not None:
        updates.append("first_name = :first_name")
        values["first_name"] = first_name
    if last_name is not None:
        updates.append("last_name = :last_name")
        values["last_name"] = last_name
    if gmail is not None:
        updates.append("gmail = :gmail")
        values["gmail"] = gmail
    if dob is not None:
        updates.append("dob = :dob")
        values["dob"] = dob
    if password_hash is not None:
        updates.append("password_hash = :password_hash")
        values["password_hash"] = password_hash

    if not updates:
        # No updates to perform
        return await get_user(user_id)

    query += ", ".join(updates)
    query += " WHERE user_id = :user_id RETURNING *"

    return await database.fetch_one(query=query, values=values)


# Function to insert a new pygame data into game_stat table
async def insert_game_stat(objectamount: int, pygametime: int, timetofinish: int, target1: int, target2: int):
    query = """
    INSERT INTO game_stat (objectamount, pygametime, timetofinish, target1, target2)
    VALUES (:objectamount, :pygametime, :timetofinish, :target1, :target2)
    RETURNING exp_number
    """
    values = {
        "objectamount": objectamount,
        "pygametime": pygametime,
        "timetofinish": timetofinish,
        "target1": target1,
        "target2": target2,
    }
    game_stat_entries = await database.fetch_all("SELECT exp_number FROM game_stat")
    print(f"Current game_stat entries: {game_stat_entries}")

    return await database.fetch_one(query=query, values=values)


async def get_game_stat(exp_number: int):
    query = "SELECT * FROM game_stat WHERE exp_number = :exp_number"
    return await database.fetch_one(query=query, values={"exp_number": exp_number})

async def delete_game_stat_and_related(exp_number: int):
    # Step 1: Delete related records from robot_stat
    await database.execute(
        "DELETE FROM robot_stat WHERE exp_number = :exp_number",
        values={"exp_number": exp_number}
    )

    # Step 2: Delete related records from robot_rank
    await database.execute(
        "DELETE FROM robot_rank WHERE exp_number = :exp_number",
        values={"exp_number": exp_number}
    )

    # Step 3: Delete the record from game_stat
    result = await database.fetch_one(
        "DELETE FROM game_stat WHERE exp_number = :exp_number RETURNING exp_number",
        values={"exp_number": exp_number}
    )
    return result


# Insert multiple robot stats (for 10 robots)
async def insert_robot_stat(exp_number: int, robots: list):
    query = """
    INSERT INTO robot_stat (exp_number, robot_id, robottime, robotpath)
    VALUES (:exp_number, :robot_id, :robottime, :robotpath)
    """
    for robot in robots:
        values = {
            "exp_number": exp_number,
            "robot_id": robot['robot_id'],
            "robottime": robot['robottime'],
            "robotpath": robot['robotpath']
        }
        await database.execute(query=query, values=values)

# Insert top 3 robot ranks
async def insert_robot_rank(exp_number: int, robots: list):
    query = """
    INSERT INTO robot_rank (exp_number, ranking, rtype, robot_id, robottime, robotpath)
    VALUES (:exp_number, :ranking, :rtype, :robot_id, :robottime, :robotpath)
    """
    for robot in robots:
        values = {
            "exp_number": exp_number,
            "ranking": robot["ranking"],
            "rtype": robot["rtype"],
            "robot_id": robot["robot_id"],
            "robottime": robot["robottime"],
            "robotpath": robot["robotpath"],
        }
        await database.execute(query=query, values=values)

# Function to get the next experiment number (exp_number)
async def get_next_experiment_number():
    query = "SELECT MAX(exp_number) AS max_exp_number FROM game_stat"
    result = await database.fetch_one(query=query)
    if result and result['max_exp_number'] is not None:
        return result['max_exp_number'] + 1
    else:
        return 1  # Start from 1 if there are no entries yet


async def store_token(user_id: int, token: str):
    query = """
    INSERT INTO tokens (token, user_id, timestamp) 
    VALUES (:token, :user_id, NOW())  -- Automatically insert the current timestamp
    """
    await database.execute(query=query, values={"token": token, "user_id": user_id})

async def get_user_by_token(token: str):
    query = """
    SELECT pnor.*
    FROM pnor
    JOIN tokens ON pnor.user_id = tokens.user_id
    WHERE tokens.token = :token
    """
    user = await database.fetch_one(query=query, values={"token": token})
    return user

async def delete_user(user_id: int):
    try:
        query = "DELETE FROM pnor WHERE user_id = :user_id RETURNING user_id"
        result = await database.fetch_one(query=query, values={"user_id": user_id})
        
        if result is None:
            print(f"User with ID {user_id} not found.")  # Debugging log
            return None
        
        print(f"User with ID {user_id} deleted.")  # Debugging log
        return result
    
    except Exception as e:
        print(f"Error deleting user: {str(e)}")  # Debugging log
        return None

# Function to authenticate user by factory ID and password
async def authenticate_user(factory_id: str, password: str):
    query = "SELECT * FROM pnor WHERE factory_id = :factory_id"
    user = await database.fetch_one(query=query, values={"factory_id": factory_id})

    if user and pwd_context.verify(password, user["password_hash"]):
        return user  # Return the user if password matches
    return None  # Return None if authentication fails
