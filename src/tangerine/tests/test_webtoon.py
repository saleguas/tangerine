import sys, os, shutil

# add the ../pages to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pages')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess


def clear_test_dir():
    download_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_dir'))
    # remove all files in the test_dir
    for filename in os.listdir(download_path):
        file_path = os.path.join(download_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def test_get_chapter_amount():
    from download_webtoon import get_chapter_amount
    url = 'https://www.webtoons.com/en/romance/til-debt-do-us-part/list?title_no=3115'

    assert get_chapter_amount(url) == 9

def test_download_webtoon():
    from download_webtoon import download_webtoon_series
    manga_url = 'https://www.webtoons.com/en/challenge/short-stories/list?title_no=270769&page=1'
    local_url = 'test_dir'

    command = download_webtoon_series(manga_url, local_url)
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()

    assert os.path.isdir(os.path.join(local_url, 'short-stories'))
    assert len(os.listdir(os.path.join(local_url, 'short-stories'))) == 15
if __name__ == "__main__":
    test_download_webtoon()
