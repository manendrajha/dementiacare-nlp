import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncMongoClient(MONGODB_URL)

database = client[DATABASE_NAME]


async def connect_to_mongodb():
    await client.admin.command("ping")
    print("Connected to MongoDB successfully!")


async def close_mongodb_connection():
    await client.close()
    print("MongoDB connection closed.")