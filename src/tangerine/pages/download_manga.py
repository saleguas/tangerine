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
    soup = r.text
    soup = soup.split('vm.Chapters = [{')[1]
    soup = soup.split(':"')[1]
    soup = soup.split('",')[0]
    if soup[:2] == '10':
        soup = soup[2:]
    else:
        soup = soup[1:]
    if soup[-1] == '0':
        soup = soup[:-1]

    return soup


def get_download_path(url, download_path):
    download_path = os.path.abspath(download_path)
    folder_name = url.split('/')[-1]
    download_path = os.path.join(download_path, folder_name)
    return download_path


def download_series(url, raw_path, container):
    logtxtbox = container.empty()
    logtxt = 'Downloading ' + url.split('/')[-1] + '...\n'
    logtxtbox.text_area("Logging: ", logtxt, height=500)
    # for i in range(10000):
    #     logtxt = logtxt + '\n' + str(i)
    #     logtxtbox.text_area("Logging: ", logtxt, height = 500)
    #     time.sleep(1)

    # for c in iter(lambda: process.stdout.read(1), b''):
    #     sys.stdout.buffer.write(c)
    raw_path = os.path.abspath(raw_path)
    print('----------------------------------', raw_path)
    process = subprocess.Popen('manga-py "{}" -d "{}"'.format(url, raw_path), stdout=subprocess.PIPE)
    print(raw_path)
    command = 'manga-py "{}" -d "{}"'.format(url, raw_path)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    download_path = get_download_path(url, raw_path)
    # os.mkdir(download_path)
    total_chapters = get_chapter_amount(url)
    progress = check_download_progress(total_chapters, download_path)

    while progress[1] < int(total_chapters):
        progress = check_download_progress(total_chapters, download_path)
        if "{}/{}".format(progress[1], total_chapters) in logtxt:
            pass
        else:
            logtxt = logtxt + '\n' + progress[0]
            logtxtbox.text_area("Logging: ", logtxt, height=500)
            print(progress[0])
        time.sleep(1)
    logtxt = logtxt + '\n' + 'Download Complete!'
    logtxtbox.text_area("Logging: ", logtxt, height=500)


def app():
    st.markdown('## Download a Manga')
    st.markdown('This app will download a series from [mangasee123.com](https://mangasee123.com)')
    container = st.container()
    manga_url = container.text_input("Enter the MangaSee123 URL", "https://mangasee123.com/manga/Tokyo-Revengers")
    download_path = container.text_input("Enter the download path", settings.LIBRARY_PATH)
    start_button = st.button("Start Download")
    if start_button:
        download_series(manga_url, download_path, container)

# print(get_chapter_amount('https://mangasee123.com/manga/Kimetsu-No-Yaiba'))
# print(get_chapter_amount('https://mangasee123.com/manga/One-Piece'))
# download_series('https://mangasee123.com/manga/Kimetsu-No-Yaiba', '.', '')
# sudo manga-py "$url"
