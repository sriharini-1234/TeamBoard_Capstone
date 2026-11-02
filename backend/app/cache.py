import hashlib
import json
import time

def make_etag(payload) -> str:
    raw = json.dumps(payload, sort_keys=True).encode()
    return '"' + hashlib.sha256(raw).hexdigest()[:16] + '"'

class TTLCache:
    def __init__(self, ttl: float = 30):
        self.ttl = ttl
        self.data = {}

    def get(self, key):
        item = self.data.get(key)
        if item and time.monotonic() - item[0] < self.ttl:
            return item[1]
        self.data.pop(key, None)
        return None

    def set(self, key, value):
        self.data[key] = (time.monotonic(), value)

    def clear(self):
        self.data.clear()
