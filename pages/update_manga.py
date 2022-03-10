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
    return files

path = os.path.abspath('../Tokyo-Revengers/')
print(get_local_chapters(path))
def find_missing_chapters(local_url, manga_url):
    total_chapters = download_manga.get_total_chapters(manga_url)


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
