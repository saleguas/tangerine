import streamlit as st
import settings
from pages.download_manga import download_series

def show_download_new_series_form(go=False):
    global form, container
    form.empty()
    container.empty()
    manga_url = container.text_input("Enter the MangaSee123 URL", "https://mangasee123.com/manga/Tokyo-Revengers")
    download_path = container.text_input("Enter the download path", settings.LIBRARY_PATH)
    start_button = st.button("Start Download", on_click=None)
    if start_button:
        show_download_new_series_form(go=True)
    if go:
        download_series(manga_url, download_path, container)


def show_update_series_form():
    global form, container
    pass


def show_repair_series_form():
    global form, container
    pass


st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("🎓 dragonfruit")
container = st.container()
form = container.form(key="form")

st.write(
    "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
)

selected_option = form.selectbox("What do you want to do?",
                                 ['Download new series', 'Update a series', 'Repair a series'])
form.empty()
container.empty()
manga_url = form.text_input("Enter the MangaSee123 URL", "https://mangasee123.com/manga/Tokyo-Revengers")
download_path = form.text_input("Enter the download path", settings.LIBRARY_PATH)
# logtxtbox = form.empty()
# logtxt = 'start'
# logtxtbox.text_area("Logging: ", "start", height = 500)
# for i in range(10000):
#     logtxt = logtxt + '\n' + str(i)
#     logtxtbox.text_area("Logging: ", logtxt, height = 500)
#     time.sleep(1)
submit = form.form_submit_button("Continue")
if submit:
    if selected_option == 'Download new series':
            download_series(manga_url, download_path, container)
    elif selected_option == 'Update a series':
        show_update_series_form()
    elif selected_option == 'Repair a series':
        show_repair_series_form()

# f = st.form()
#
# # make a program that downloads and manages a library of manga files
# form = f.form("template_form")
# selected_option = form.selectbox("What do you want to do?", ["Update an existing series", "Download a new Series", "Repair an existing Series"])
#
# print(selected_option)
# loaded_form = form.empty()
# if selected_option == "Update an existing series":
#     loaded_form = form.text_input("Enter the name of the series you want to update:", "")
# elif selected_option == "Download a new Series":
#     loaded_form = form.text_input("Enter the name of the series you want to download:", "")
# elif selected_option == "Repair an existing Series":
#     loaded_form = form.text_input("Enter the name of the series you want to repair:", "")
#
# submit = form.form_submit_button("Generate PDF")
# reset = form.form_submit_button("Reset")
# if reset:
#     form.empty()
# if submit:
#
#     st.balloons()

# right.success("🎉 Your diploma was generated!")
# st.write(html, unsafe_allow_html=True)
# st.write("")
# right.write("Here's the template we'll be using:")
#
# right.image("template.png", width=300)
#
# env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
# template = env.get_template("template.html")
#
#
# left.write("Fill in the data:")
# form = left.form("template_form")
# student = form.text_input("Student name")
# course = form.selectbox(
#     "Choose course",
#     ["Report Generation in Streamlit", "Advanced Cryptography"],
#     index=0,
# )
#
# output = student + " - " + course
#

#
# grade = form.slider("Grade", 1, 100, 60)
