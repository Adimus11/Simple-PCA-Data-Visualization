import redis
import pickle
from config import (
    REDIS_URL,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PREFIX
)

client = None

def get_client():
    global client
    if client is None:
        client = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB)
    return client

def clear_all():
    redis_client = get_client()
    keys = redis_client.keys(f"{REDIS_PREFIX}:*")
    for key in keys:
        redis_client.delete(key)

def store_object(data, id):
    redis_client = get_client()
    data = pickle.dumps(data)
    redis_client.set(f"{REDIS_PREFIX}:{id}", data)

def get_objects():
    objects = []
    redis_client = get_client()
    keys = redis_client.keys(f"{REDIS_PREFIX}:*")
    for key in keys:
        data = redis_client.get(key)
        id = key.decode("utf-8").split(":")[1]
        unpickled_data = pickle.loads(data)
        unpickled_data["id"] = id
        objects.append(unpickled_data)

    return objects