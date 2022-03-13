import os, sys
import time
import atexit
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler

LIBRARY_PATH = '~/library/'
DOWNLOAD_QUEUE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_queue.csv'))

def check_download_finished(total_chapters, download_path):
    chapter_amount = len(os.listdir(download_path))
    # get the size in mb of the folder
    print(chapter_amount, total_chapters)
    print(chapter_amount == total_chapters)
    return int(chapter_amount) == int(total_chapters)

def fill_folder(amt, folder):
    for i in range(amt):
        file_name = i
        if i < 10:
            file_name = '0' + str(i)
        if i < 100:
            file_name = '0' + str(i)
        with open(os.path.join(folder, 'vol_{}-1.zip'.format(file_name)), 'w') as f:
            f.write('test')

fill_folder(os.path.abspath("pigpen"))
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
            series_download_path = os.path.join(download_path, series_name)
            print(series_url)
            print(command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            progress = check_download_finished(total_chapters, series_download_path)
            while not progress:
                progress = check_download_finished(total_chapters, series_download_path)
                time.sleep(5)
    with open (DOWNLOAD_QUEUE_FILE, 'w') as f:
        for line in lines[1:]:
            f.write(line)

download_request()

def make_scheduler(seconds):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=download_request, trigger="interval", seconds=seconds)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return scheduler

