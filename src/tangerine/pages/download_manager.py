import errno
import os, sys
import streamlit as st
import pandas as pd
import time
import atexit
import subprocess
import shutil
import zipfile

sys.path.append(os.path.abspath('..'))
import settings

from apscheduler.schedulers.background import BackgroundScheduler

def check_download_finished(total_chapters, download_path, download_type):
    chapter_amount = len(os.listdir(download_path))
    if download_type == 'WD':
        chapter_amount += 1
    print(download_path)
    # get the size in mb of the folder
    print(chapter_amount, total_chapters)
    return int(chapter_amount) >= int(total_chapters)


def fill_folder(amt, folder):
    for i in range(amt):
        file_name = i
        if i < 10:
            file_name = '0' + str(i)
        if i < 100:
            file_name = '0' + str(file_name)
        with open(os.path.join(folder, 'vol_{}-1.zip'.format(file_name)), 'w') as f:
            f.write('test')

# fill_folder(248, '../Tokyo-Revengers')

# 115, 125
# def chapify_folder(folder_path):
#     # turn each folder into a zip with name chapter_number
#     for folder in os.listdir(folder_path):
#         if os.path.isdir(os.path.join(folder_path, folder)):
#             try:
#                 print(folder)
#                 folder_name = folder
#                 if int(folder_name) < 10:
#                     folder_name = '0' + str(folder_name)
#                 if int(folder_name) < 100:
#                     folder_name = '0' + str(folder_name)
#                 zip_name = 'vol_{}-1'.format(folder_name)
#                 shutil.make_archive(os.path.join(folder_path, zip_name), 'zip', os.path.join(folder_path, folder))
#             except Exception as e:
#                 print(e)
#     # remove the folders
#     time.sleep(5)
#     for folder in os.listdir(folder_path):
#         if os.path.isdir(os.path.join(folder_path, folder)):
#             shutil.rmtree(os.path.join(folder_path, folder))


def download_request():
    # check to see if download_queue has any items
    # if so, download the first item
    # if not, do nothing
    with open (settings.DOWNLOAD_QUEUE_FILE, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            # download the first item
            line = lines[0].split(',')
            # write series name, series url, download path, download type, total chapters,

            series_name, series_url, series_download_path, download_type, total_chapters,command = line[0], line[1], line[2], line[3], line[4], line[5]
            print(series_url)
            print(command)
            if not os.path.exists(series_download_path):
                os.makedirs(series_download_path)
            # process = subprocess.Popen(command, stdout=subprocess.PIPE)


            # with open (settings.DOWNLOAD_QUEUE_FILE, 'w') as f:
            #     for line in lines[1:]:
            #         f.write(line)

# chapify_folder('../pigpen')

def make_scheduler(seconds):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=download_request, trigger="interval", seconds=seconds)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return scheduler


def app():
    st.markdown('## View Downloads & Tasks')
    st.markdown('View all pending downloads and status here')
    container = st.container()
    # Get the list of all pending downloads
    tasks = pd.read_csv(settings.DOWNLOAD_QUEUE_FILE, header=None)
    print(tasks)
    # drop the 2nd column
    # eries_name, series_url, download_path, download_type, total_chapters, command
    try:
        tasks.columns = ["Series Name", "Series URL", "Download Path", "Download type", "Progress", "Command", "Current"]
        # tasks = tasks.drop(columns=["Series URL", "Download Path", "Command"])
        # set current to the amount of chapters downloaded
        for index, row in tasks.iterrows():
            row['Current'] = len(os.listdir(row['Download Path']))
            row['Progress'] = "{} / {}".format(row['Current'], row['Progress'])
            tasks.loc[index] = row
            print("Progress for {}: {}".format(row['Series Name'], row['Progress']))
        print(tasks)
        tasks = tasks.drop(columns=["Series URL", "Download Path", "Command", "Current"])
        container.table(tasks)
    except Exception as e:
        print(e)
        st.write("No downloads pending.")

if __name__ == '__main__':
    pass


# python ./webtoon_download/src/webtoon_downloader.py "https://www.webtoons.com/en/thriller/pigpen/list?title_no=2275"
