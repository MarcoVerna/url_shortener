import datetime

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