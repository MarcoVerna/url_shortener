from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client["url_shortener"]

app = FastAPI()