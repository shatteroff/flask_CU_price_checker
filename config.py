import os

import redis


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is_super-hard-secret_key'
    hour_for_update = 14
    # conn_local = redis.Redis(db=1)
    conn_heroku = redis.from_url(os.environ.get("REDIS_URL"))
