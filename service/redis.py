import redis
from config import (
    REDIS_URL,
    REDIS_PORT,
    REDIS_DB 
)

client = None

def get_client():
    if client is None:
        client = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB)
    return client