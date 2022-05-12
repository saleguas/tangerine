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
    url1 = "https://mangasee123.com/manga/G-Edition"
    url2 = "https://mangasee123.com/manga/20th-Century-Boys"
    assert int(get_chapter_amount(url1)) == 16
    assert int(get_chapter_amount(url2)) == 249



def test_download_manga():
    from download_manga import download_series

    manga_url = "https://mangasee123.com/manga/full-Moon"
    download_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_dir'))
    command = download_series(manga_url, download_path)

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    # wait for the process to finish
    process.wait()
    # get the output

    downloaded_path = os.path.join(download_path, "full-Moon")
    assert len(os.listdir(downloaded_path)) == 6
    clear_test_dir()

def test_missing_chapters():
    from update_manga import find_missing_chapters

    manga_url = "https://mangasee123.com/manga/full-Moon"
    local_url = os.path.abspath(os.path.join(os.path.dirname(__file__), 'update_manga_test_dir', "full-Moon"))
    missing_chapters = find_missing_chapters(local_url, manga_url)
    print(missing_chapters)
    assert len(missing_chapters) == 3
    assert missing_chapters[0] == 3
    assert missing_chapters[1] == 5
    assert missing_chapters[2] == 6

def test_update_manga():
    from update_manga import update_series

    manga_url = "https://mangasee123.com/manga/full-Moon"
    local_url = os.path.abspath(os.path.join(os.path.dirname(__file__), 'update_manga_test_dir', "full-Moon"))

    commands = update_series(manga_url, local_url)
    for command in commands:
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        # wait for the process to finish
        process.wait()
        # get the output

    assert len(os.listdir(local_url)) == 6
    # delete files vol_002-1.zip and vol_004-1.zip from the local_url
    os.remove(os.path.join(local_url, "vol_003-1.zip"))
    os.remove(os.path.join(local_url, "vol_005-1.zip"))
    os.remove(os.path.join(local_url, "vol_006-1.zip"))


if __name__ == "__main__":
    test_get_chapter_amount()
