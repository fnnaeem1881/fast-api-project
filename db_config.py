from databases import Database

DATABASE_URL = "mysql://root@localhost/fastapi"
database = Database(DATABASE_URL)

async def connect_to_database():
    await database.connect()

async def close_database_connection():
    await database.disconnect()