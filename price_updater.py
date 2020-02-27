import datetime

from config import Config
from redis_helper import RedisHelper

redis_helper = RedisHelper()


def update_prices():
    print(f'{datetime.datetime.now()}\tUpdate started')
    conn = Config.conn
    redis_helper.update_date()
    redis_helper.load_prices(conn)
    redis_helper.add_product(conn)
    conn.close()
    print(f'{datetime.datetime.now()}\tUpdate ended')


update_prices()
