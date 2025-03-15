from pymongo import ReturnDocument

class ShortCodeDispenser():
    db = None
    alphabet = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    
    def __init__(self, db):
        self.db = db

    def generate_short_code(self, id: int) -> str:
        if id == 0:
            return self.alphabet[0]
        arr = []
        arr_append = arr.append  # Extract bound-method for faster access.
        _divmod = divmod  # Access to locals is faster.
        base = len(self.alphabet)
        while id:
            id, rem = _divmod(id, base)
            arr_append(self.alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    def get_next(self) -> str:
        counter = self.db.counters.find_one_and_update(
            {"_id": "url_counter"},
            {"$inc": {"count": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        new_id = counter["count"]
        return self.generate_short_code(new_id)