import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from config import Config
from redis_helper import RedisHelper
from table import Table

scheduler = BackgroundScheduler()
redis_helper = RedisHelper()
table = Table()


@scheduler.scheduled_job('cron', hour=Config.hour_for_update, minute=Config.minute_for_update)
def update_prices():
    print(datetime.datetime.now())
    conn2 = Config.conn
    redis_helper.update_date()
    redis_helper.load_prices(conn2)
    redis_helper.add_product(conn2)
    table.update(conn2)
    conn2.close()


scheduler.start()
