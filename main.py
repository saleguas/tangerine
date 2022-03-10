import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('pages'))

from pages import download_manga
from pages import update_manga
from multipage import MultiPage
# Define the multipage class to manage the multiple apps in our program


app = MultiPage()

# Title of the main page
st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("Download a series", download_manga.app)
app.add_page("Update a series", update_series.app)

# The main app
app.run()