import os
import sys

# Allow running as a script directly by setting _package_ properly.
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "src"

import argparse
import datetime
import pymongo
from pymongo import MongoClient
from .ShortCodeDispenser import ShortCodeDispenser

MONGODB_CONNECTION_STRING = os.environ.get("MONGODB_CONNECTION_STRING")
client = MongoClient(MONGODB_CONNECTION_STRING)
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

    def to_dict(self):
        return {
            "long_url": self.long_url,
            "short_code": self.short_code,
            "created_at": self.created_at,
            "expiration_seconds": self.expiration_seconds
        }


class Response():
    url: UrlMapping
    message: str

    def __init__(self, url: UrlMapping, message: str):
        self.url = url
        self.message = message


def minifyUrl(db, long_url, expiration_seconds):
    short_code = ShortCodeDispenser(db).get_next()
    mapping = UrlMapping(long_url, short_code, datetime.datetime.now(datetime.UTC), expiration_seconds)
    db.urls.insert_one(mapping.to_dict())
    
    response = Response(mapping, f"Shortened URL: https://myurlshortener.com/{short_code}")
    return response

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
