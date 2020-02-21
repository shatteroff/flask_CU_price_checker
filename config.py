import os

import redis


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is_super-hard-secret_key'
    hour_for_update = 12
    minute_for_update = 20
    try:
        conn = redis.from_url(os.environ.get("REDIS_URL"))
    except ValueError:
        conn = redis.Redis(db=1)
