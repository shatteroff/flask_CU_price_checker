import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is_super-hard-secret_key'
    hour_for_update = 17
