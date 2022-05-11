import os
import subprocess
import sys
import time

import streamlit as st
import settings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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


def clean_download_chapters(chapters):
    # find start chapter and length of ascending list of chapters
    # [1, 2, 3, 6, 7] -> [(1, 3), (6, 2)]
    # [1, 2, 3, 4, 5, 6, 7] -> [(1, 7)]
    result = []
    counter = 1
    for i in range(1, len(chapters)):
        if chapters[i] - chapters[i - 1] == 1:
            counter += 1
        else:
            result.append((chapters[i - counter], counter))
            counter = 1
    result.append((chapters[-counter], counter))
    return result


def format_download_command(chapter_start, chapter_length, manga_url, local_url):
    # get folder name of local url
    local_url = os.path.dirname(local_url)
    command = 'manga-py --skip-volumes {} --max-volumes {} "{}" -d "{}"'.format(chapter_start, chapter_length, manga_url,
                                                                            local_url)
    return command


def check_download_progress(total_chapters, download_path):
    pass

    # logtxtbox = container.empty()
    # logtxt = 'Downloading ' + url.split('/')[-1] + '...\n'
    # logtxtbox.text_area("Logging: ", logtxt, height=500)
    # for i in range(10000):
    #     logtxt = logtxt + '\n' + str(i)
    #     logtxtbox.text_area("Logging: ", logtxt, height = 500)
    #     time.sleep(1)


def update_series(manga_url, local_url, container=None):
    # logtxtbox = container.empty()
    # logtxt = 'Downloading ' + manga_url.split('/')[-1] + '...\n'
    # logtxtbox.text_area("Logging: ", logtxt, height=500)

    local_url = os.path.abspath(local_url)
    chapters_to_download = find_missing_chapters(local_url, manga_url)
    cleaned_chapters = clean_download_chapters(chapters_to_download)
    print(cleaned_chapters)

    commands = []
    for chapter_start, chapter_length in cleaned_chapters:
        command = format_download_command(chapter_start-1, chapter_length, manga_url, local_url)
        with open(settings.DOWNLOAD_QUEUE_FILE, 'a') as f:
            # series_name, series_url, download_path, download_type, total_chapters, command
            f.write(manga_url.split('/')[-1] + ',')
            f.write(manga_url + ',')
            f.write(local_url + ',')
            f.write('MU,')
            f.write(download_manga.get_chapter_amount(manga_url) + ',')
            f.write(command + ',\n')
        commands.append(command)

    return commands


# update_series('https://mangasee123.com/manga/Tokyo-Revengers', '../Tokyo-Revengers', st)
# update_series('https://mangasee123.com/manga/Tokyo-Revengers', '../Tokyo-Revengers', st)

def app():
    st.markdown('## Update a Series')
    st.markdown(
        'This app will update a series of manga from a given url. This means it will download any mising chapters, including new releases.')
    container = st.container()
    local_url = container.text_input("Enter the local manga URL", "{}Tokyo-Revengers".format(settings.LIBRARY_PATH))
    manga_url = container.text_input("Enter the MangaSee123 URL", "https://mangasee123.com/manga/Tokyo-Revengers")
    start_button = st.button("Start Download")
    if start_button:
        update_series(manga_url, local_url, container)
# print(get_chapter_amount('https://mangasee123.com/manga/Kimetsu-No-Yaiba'))
# print(get_chapter_amount('https://mangasee123.com/manga/One-Piece'))
# download_series('https://mangasee123.com/manga/Kimetsu-No-Yaiba', '.', '')
# sudo manga-py "$url"
