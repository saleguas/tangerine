import os, sys
import time
import atexit
import subprocess
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('pages'))
import download_manga

from apscheduler.schedulers.background import BackgroundScheduler

LIBRARY_PATH = '~/library/'
DOWNLOAD_QUEUE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_queue.csv'))

def download_request():
    # check to see if download_queue has any items
    # if so, download the first item
    # if not, do nothing
    with open (DOWNLOAD_QUEUE_FILE, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            # download the first item
            line = lines[0].split(',')
            # write series name, series url, download path, download type, total chapters,

            series_name, series_url, download_path, download_type, total_chapters,command = line[0], line[1], line[2], line[3], line[4], line[5]

            # process = subprocess.Popen(command, stdout=subprocess.PIPE)
            # download_path = download_manga.get_download_path(url, raw_path)
            # # os.mkdir(download_path)
            # total_chapters = download_manga.get_chapter_amount(url)
            # progress = download_manga.check_download_progress(total_chapters, download_path)
            #
            # while progress[1] < int(total_chapters):
            #     progress = download_manga.check_download_progress(total_chapters, download_path)
            #     if "{}/{}".format(progress[1], total_chapters) in logtxt:
            #         pass
            #     else:
            #         logtxt = logtxt + '\n' + progress[0]
            #         logtxtbox.text_area("Logging: ", logtxt, height=500)
            #         print(progress[0])
            #     time.sleep(1)
            # logtxt = logtxt + '\n' + 'Download Complete!'
            # logtxtbox.text_area("Logging: ", logtxt, height=500)



def make_scheduler(seconds):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=seconds)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return scheduler

