import os, sys
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def make_scheduler(seconds):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=seconds)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return scheduler

LIBRARY_PATH = '~/library/'
DOWNLOAD_QUEUE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_queue.csv'))