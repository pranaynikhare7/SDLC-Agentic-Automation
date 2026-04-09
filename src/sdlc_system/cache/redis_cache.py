import json
from typing import TypedDict, Any, Dict, Literal, Optional

import redis
from src.sdlc_system.state.state_file import  SDLCState
from upstash_redis import Redis

from pydantic import BaseModel, Field
import os

from dotenv import load_dotenv
load_dotenv()

## Upstash Redis Client Configuraion
REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
redis_client = redis = Redis(url=REDIS_URL, token=REDIS_TOKEN)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):

        # Check if the object is any kind of Pydantic model
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        
        # Or check for specific classes if needed
        return super().default(obj)



def save_state_to_redis(task_id: str, state: SDLCState):
    """Save the state to Redis."""
    state = json.dumps(state, cls=CustomEncoder)
    redis_client.set(task_id, state)

    # Set expiration for 24 hours
    redis_client.expire(task_id, 86400)

def get_state_from_redis(task_id: str) -> Optional[SDLCState]:
    """ Retrieves the state from redis """
    state_json = redis_client.get(task_id)
    if not state_json:
        return None
    
    state_dict = json.loads(state_json)[0]
    return SDLCState(**state_dict)

def delete_from_redis(task_id: str):
    """ Delete from redis """
    redis_client.delete(task_id)

def flush_redis_cache():
    """ Flushes the whole cache"""

    # Clear all keys in all databases
    redis_client.flushall()
