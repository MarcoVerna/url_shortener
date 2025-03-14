from motor.motor_asyncio import AsyncIOMotorClient
import os
import argparse
import datetime


MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client["url_shortener"]


class UrlMapping():
    _id: int
    long_url: str
    short_code: str
    created_at: datetime.datetime
    expiration_seconds: int

    def __init__(self, long_url: str, short_code: str, created_at: datetime.datetime, expiration_seconds: int):
        self.long_url = long_url
        self.short_code = short_code
        self.created_at = created_at
        self.expiration_seconds = expiration_seconds

class Response():
    url: UrlMapping
    message: str

    def __init__(self, url: UrlMapping, message: str):
        self.url = url
        self.message = message


def minifyUrl(db, long_url, expiration_seconds):
    pass

def expandUrl(db, short_code):
    pass

def main():
    parser = argparse.ArgumentParser(description="URL Shortener Tool")
    parser.add_argument('--minify', type=str, help='Complete URL to shorten')
    parser.add_argument('--expand', type=str, help='Shortened URL to expand')
    parser.add_argument('--expiration', type=int, default=3600, help='Expiration time in seconds')
    args = parser.parse_args()

    if args.minify:
        response = minifyUrl(db, args.minify, args.expiration)
    elif args.expand:
        response = expandUrl(db, args.expand)
    else:
        response = Response(None,"Please provide either --minify or --expand parameter.")
    
    print(response.message)

if __name__ == "__main__":
    main()
