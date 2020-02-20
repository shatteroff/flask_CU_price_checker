from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
print(f'{datetime.now()}')
sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print(f'{datetime.now()} This job is run every three minutes.')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=15, minute= 46)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
