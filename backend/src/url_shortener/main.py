from motor.motor_asyncio import AsyncIOMotorClient
import os
import argparse
import datetime

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client["url_shortener"]

def main():
    parser = argparse.ArgumentParser(description="URL Shortener Tool")
    args = parser.parse_args()

    print('working')

if __name__ == "__main__":
    main()


