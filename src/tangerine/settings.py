import os, sys


# get the environment variable LIBRARY_PATH
LIBRARY_PATH = os.environ.get('LIBRARY_PATH')
DOWNLOAD_QUEUE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_queue.csv'))
