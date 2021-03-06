import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from config import Config
from redis_helper import RedisHelper

scheduler = BlockingScheduler()
redis_helper = RedisHelper()


@scheduler.scheduled_job('cron', misfire_grace_time=3000, hour=Config.hour_for_update, minute=Config.minute_for_update)
def update_prices():
    print(f'{datetime.datetime.now()}\tUpdate started')
    conn = Config.conn
    redis_helper.update_date()
    redis_helper.load_prices(conn)
    redis_helper.add_product(conn)
    conn.close()
    print(f'{datetime.datetime.now()}\tUpdate ended')


@scheduler.scheduled_job('interval', minutes=5)
def timed_job():
    print('Test scheduler is run every 5 minutes.')


scheduler.start()
