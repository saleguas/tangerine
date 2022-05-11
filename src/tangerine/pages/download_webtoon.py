import os
import subprocess
import requests
import time
import streamlit as st
import settings
from pathlib import Path


def get_folder_size(download_path):
    root_directory = Path(download_path)
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())


def check_download_progress(total_chapters, download_path):
    chapter_amount = len(os.listdir(download_path))
    # get the size in mb of the folder
    folder_size = get_folder_size(download_path) / 1000000.0
    output_str = '| Downloading: ' + str(chapter_amount) + '/' + str(total_chapters)
    output_str = output_str + '\n' + 'Size: ' + str(folder_size) + ' MB'
    return (output_str, chapter_amount, folder_size)


def get_chapter_amount(url):
    r = requests.get(url)
    val = r.text
    index = val.find('<li id="episode_')
    val = val[index:]
    val = val.split('<li id="episode_')
    val = val[1].split('"')
    return int(val[0])


def get_download_path(manga_url, download_path):
    folder_name = manga_url.split('/')[-2]
    download_path = os.path.join(download_path, folder_name)
    return download_path


def download_webtoon_series(manga_url, local_url):
    download_path = get_download_path(manga_url, local_url)

    program_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'webtoon_download', 'webtoon_downloader.py'))
    command = 'python "{}" "{}" --dest "{}" --seperate'.format(program_path, manga_url, download_path)
    with open(settings.DOWNLOAD_QUEUE_FILE, 'a') as f:
        # series_name, series_url, download_path, download_type, total_chapters, command
        f.write(manga_url.split('/')[-2] + ',')
        f.write(manga_url + ',')
        f.write(download_path + ',')
        f.write('WD,')
        f.write(str(get_chapter_amount(manga_url)) + ',')
        f.write(command + ',\n')

    return command



    # process = subprocess.Popen(
    #     command,
    #     stdout=subprocess.PIPE)
    # total_chapters = get_chapter_amount(url)
    # progress = check_download_progress(total_chapters, download_path)
    #
    # while progress[1] < int(total_chapters):
    #     progress = check_download_progress(total_chapters, download_path)
    #     if "{}/{}".format(progress[1], total_chapters) in logtxt:
    #         pass
    #     else:
    #         logtxt = logtxt + '\n' + progress[0]
    #         logtxtbox.text_area("Logging: ", logtxt, height=500)
    #         print(progress[0])
    #     time.sleep(1)
    # logtxt = logtxt + '\n' + 'Download Complete!'
    # logtxtbox.text_area("Logging: ", logtxt, height=500)


def app():
    st.markdown('## Download a Webtoon Series')
    st.markdown('This app will download a series from [webtoons.com](https://webtoons.com)')
    container = st.container()
    manga_url = container.text_input("Enter the webtoon URL",
                                     "https://www.webtoons.com/en/thriller/pigpen/list?title_no=2275")
    download_path = container.text_input("Enter the download path", settings.LIBRARY_PATH)
    start_button = st.button("Start Download")
    if start_button:
        download_webtoon_series(manga_url, download_path, container)

# python ./webtoon_download/src/webtoon_downloader.py "https://www.webtoons.com/en/thriller/pigpen/list?title_no=2275"
