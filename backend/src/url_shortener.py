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
SHORTENED_URL_PREFIX = "https://myurlshortener.com/"
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

    def from_dict(data):
        return UrlMapping(
            data["long_url"],
            data["short_code"],
            data["created_at"],
            data["expiration_seconds"]
        )

class Response():
    url: str
    message: str
    mapping: UrlMapping
    
    def __init__(self, url: str = "", message: str = "", mapping: UrlMapping = None):
        self.url = url
        self.message = message
        self.mapping = mapping


def minifyUrl(db, long_url, expiration_seconds):
    now = datetime.datetime.now(datetime.UTC)
    validity_window = now - datetime.timedelta(seconds=expiration_seconds)
    alreadyExisting = db.urls.find_one({
        "long_url": long_url,
        "created_at": {"$gte": validity_window}
        })

    if alreadyExisting:
        short_code = alreadyExisting["short_code"]
        mapping = UrlMapping.from_dict(alreadyExisting)
    else:
        short_code = ShortCodeDispenser(db).get_next()
        mapping = UrlMapping(long_url, short_code, datetime.datetime.now(datetime.UTC), expiration_seconds)
        db.urls.insert_one(mapping.to_dict())
    
    short_url = f"{SHORTENED_URL_PREFIX}{short_code}"
    return Response(short_url, f"Shortened URL: {short_url}", mapping)

def expandUrl(db, short_url):
    now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    short_code = short_url.rstrip('/').split('/')[-1]
    urlFound = db.urls.find_one({"short_code": short_code})

    if urlFound:
        created_at = urlFound["created_at"]
        expiration_seconds = urlFound["expiration_seconds"]

        print('TULULULU')
        print(now)
        print(created_at + datetime.timedelta(seconds=expiration_seconds))

        if created_at + datetime.timedelta(seconds=expiration_seconds) >= now:
            print('BAKAKAKA')
            long_url = urlFound["long_url"]
            mapping = UrlMapping.from_dict(urlFound)
            return Response(long_url, f"Original URL: {long_url}", mapping)

    return Response('', "Error: Shortened URL does not exist or has expired.", None)

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
        response = Response('',"Please provide either --minify or --expand parameter.", None)
    
    print(response.message)
    return response

if __name__ == "__main__":
    main()
