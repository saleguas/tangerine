import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# add the path ./pages to the sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages'))


from pages import download_manga
from pages import update_manga
from pages import download_webtoon
from pages import download_manager
# from pages import update_webtoon
from multipage import MultiPage
import settings

# Define the multipage class to manage the multiple apps in our program

scheduler = download_manager.make_scheduler(10)

app = MultiPage()
st.set_page_config(
    layout="centered",
)
# Title of the main page
st.title("Tangerine")

# Add all your applications (pages) here
app.add_page("Download a Manga", download_manga.app)
app.add_page("Update a Manga", update_manga.app)
app.add_page("Download a Webtoon", download_webtoon.app)
app.add_page("View Downloader Manager", download_manager.app)

# app.add_page("Update a Webtoon series", update_webtoon.app)

# The main app
app.run()

# C:\Users\user\Documents\GitHub\tangerine
