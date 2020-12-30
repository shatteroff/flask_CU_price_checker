import os

import redis


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is_super-hard-secret_key'
    hour_for_update = 16
    minute_for_update = 0
    try:
        conn = redis.from_url(os.environ.get("REDIS_URL"))
        hour_for_update = hour_for_update - 3
    except ValueError:
        conn = redis.from_url(
            "redis://h:p4897b4bc76e07a5e0697004c07a3254503a2663a6398b2b3b17989b1a62acdfd@ec2-54-74-161-95.eu-west-1.compute.amazonaws.com:15969")
        # conn = redis.Redis(db=1)
