import os
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

import streamlit as st
import settings
sys.path.append(os.path.abspath('.'))
import download_manga

def get_local_chapters(local_url):
    files = os.listdir(local_url)
    # get only the chapter numbers from name like vol_001-1.zip to 1
    chapters = [int(file.split('_')[1].split('-')[0]) for file in files]
    return chapters


def find_missing_chapters(local_url, manga_url):
    total_chapters = int(download_manga.get_chapter_amount(manga_url))
    local_chapters = get_local_chapters(local_url)
    # find which chapters are missing
    missing_chapters = [i for i in range(1, total_chapters + 1) if i not in local_chapters]
    return missing_chapters

print(find_missing_chapters('../Tokyo-Revengers', 'https://mangasee123.com/manga/Tokyo-Revengers'))


def check_download_progress(total_chapters, download_path):
    pass



def update_series(url, download_path, container):
    pass



def app():
    st.markdown('## Update a Series')
    st.markdown('This app will update a series of manga from a given url. This means it will download any mising chapters, including new releases.')
    container = st.container()
    local_url = container.text_input("Enter the local manga URL", "{}Tokyo-Revengers".format(settings.LIBRARY_PATH))
    manga_url = container.text_input("Enter the MangaSee123 URL", "https://mangasee123.com/manga/Tokyo-Revengers")
    start_button = st.button("Start Download")
    if start_button:
        update_series(local_url, manga_url, container)
# print(get_chapter_amount('https://mangasee123.com/manga/Kimetsu-No-Yaiba'))
# print(get_chapter_amount('https://mangasee123.com/manga/One-Piece'))
# download_series('https://mangasee123.com/manga/Kimetsu-No-Yaiba', '.', '')
# sudo manga-py "$url"
