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
    from download_manga import get_chapter_amount
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

    clear_test_dir()

def test_find_missing_chapters():
    from update_webtoon import find_missing_chapters
    manga_url = 'https://www.webtoons.com/en/challenge/short-stories/list?title_no=270769&page=1'
    local_url = os.path.abspath(os.path.join(os.path.dirname(__file__), 'update_webtoon_test_dir', 'short-stories'))

    missing_chapters = find_missing_chapters(local_url, manga_url)
    # print(missing_chapters)
    assert len(missing_chapters) == 9
    assert missing_chapters[0] == 4

def test_update_webtoon():
    from update_webtoon import update_series

    manga_url = 'https://www.webtoons.com/en/challenge/short-stories/list?title_no=270769&page=1'
    local_url = os.path.join(os.path.dirname(__file__), 'update_webtoon_test_dir', 'short-stories')
    commands = update_series(manga_url, local_url)
    for command in commands:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        process.wait()

    assert len(os.listdir(local_url)) == 15
    # delete all volumes besides vol_000-cringe.zip and vol_010-cringe.zip
    for filename in os.listdir(local_url):
        if filename != 'vol_000-cringe.zip' and filename != 'vol_010-cringe.zip':
            os.remove(os.path.join(local_url, filename))



if __name__ == "__main__":
    test_update_webtoon()
