import os
import subprocess
import requests
import time
import streamlit as st
import settings
import pandas as pd
def app():
    st.markdown('## View Downloads & Tasks')
    st.markdown('View all pending downloads and status here')
    container = st.container()
    # Get the list of all pending downloads
    tasks = pd.read_csv(settings.DOWNLOAD_QUEUE_FILE, header=None)
    # drop the 2nd column
    # eries_name, series_url, download_path, download_type, total_chapters, command
    tasks.columns = ["Series Name", "Series URL", "Download Path", "Download type", "Progress", "Command"]
    tasks = tasks.drop(columns=["Series URL", "Download Path", "Command"])
    tasks['Progress'] = tasks['Progress'].apply(lambda x: "0/{}".format(x))
    print(tasks)
    container.table(tasks)




# python ./webtoon_download/src/webtoon_downloader.py "https://www.webtoons.com/en/thriller/pigpen/list?title_no=2275"
