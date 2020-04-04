import lxml.html
import os
import platform
import sys
import urllib.request
import urllib.error
import urllib.parse

from threading import Thread


ROOT_DIRECTORY = ''
URL_CACHE = set()
BROKEN_URLS = []

try:
    from progressbar import ProgressBar, SimpleProgress
    SHOW_PROGRESS_BAR = True
except ImportError:
    SHOW_PROGRESS_BAR = False


def directory_get_urls(directory):
    """Returns a list of tuples in the form (url, file_name, line_number)"""
    if not os.path.exists(directory):
        raise ValueError('Existence cannot find the directory %s' % directory)

    if not os.path.isdir(directory):
        raise ValueError('Existence requires a directory as an argument!')

    for root, subFolders, files in os.walk(directory):
        for f in files:
            if f.endswith(".html"):
                full_path = os.path.join(root, f)

                with open(full_path, 'r+') as fin:
                    for u in parse_html_urls(full_path, fin.read()):
                        yield u


def parse_html_urls(file_name, html_data):
    """Returns a list of tuples in the form (url, file_name, line_number)"""
    try:
        if not html_data:
            return

        html = lxml.html.fromstring(html_data)
        anchor_tags = html.cssselect('a')

        for a in anchor_tags:
            # A link was started but not finished, href with nothing set!
            if 'href' not in a.attrib or a.attrib['href'] == '':
                BROKEN_URLS.append(('None', file_name, a.sourceline))

            url = clean_url(a.attrib.get('href', ''))

            if is_valid_url(url):
                if url not in URL_CACHE:
                    URL_CACHE.add(url)

                    yield url, file_name, a.sourceline

    except SyntaxError:
        pass


def is_valid_url(url):
    if not url:
        return False

    if url.startswith("#"):
        return False

    if url.startswith("mailto"):
        return False

    if url.startswith("irc://"):
        return False

    return True


def clean_url(url):
    if platform.system() == "Windows":
        if url.startswith("C:\\"):
            url = url.replace("C:\\", "file:///C:/")
    else:
        if url.startswith("/"):
            # i.e. /Users/eric/src/something, /output
            root = os.path.join(os.getcwd(), ROOT_DIRECTORY)
            url = f"file://{root}{url}"

    return url


def async_check_url(url, file_name, line_number):
    try:
        urllib.request.urlopen(url).getcode()
    except urllib.error.HTTPError as e:
        if e.code == 999:
            # Linked in kicked us out!
            pass
        elif e.code == 403:
            # Well fine! We'll go elsewhere!
            BROKEN_URLS.append((url, file_name, line_number))
        else:
            raise e
    except (ValueError, urllib.error.URLError):
        BROKEN_URLS.append((url, file_name, line_number))


def check_urls(urls):
    """expected format of urls is list of tuples (url, file name, source line) i.e. ("google.com", "index.html", 32)"""
    # threads = list()
    progress_bar = None
    # progress_counter = 0

    if SHOW_PROGRESS_BAR and len(urls) > 0:

        widgets = [SimpleProgress()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(urls)).start()

    # for u in urls:
    #     t = Thread(target=async_check_url, args=(u[0], u[1], u[2]))
    #     t.start()
    #     threads.append(t)
    #
    # for thread in threads:
    #     if SHOW_PROGRESS_BAR and len(urls) > 0:
    #         progress_counter = progress_counter + 1
    #         progress_bar.update(progress_counter)
    #
    #     thread.join()
    for progress, u in enumerate(urls):
        if SHOW_PROGRESS_BAR and len(urls) > 0:
            progress_bar.update(progress)
        async_check_url(*u)

    if SHOW_PROGRESS_BAR and len(urls) > 0:
        progress_bar.finish()


def scan(directory):
    """Scans directory for bad links and returns the list of broken urls"""
    urls = list(directory_get_urls(directory))
    check_urls(urls)

    return BROKEN_URLS


def main():
    global ROOT_DIRECTORY

    if len(sys.argv) == 1:
        print('Existence requires a directory as an argument!')
        exit(-1)

    ROOT_DIRECTORY = sys.argv[1]

    print("Checking links...")

    try:
        scan(ROOT_DIRECTORY)
    except ValueError as e:
        print(e)
        exit(-1)

    if len(BROKEN_URLS) > 0:
        print("Broken links:")

        for url in BROKEN_URLS:
            print(f"    {url[1]}@{url[2]} '{url[0]}'")

        exit(-1)
    else:
        print("All of your links exist!")


if __name__ == '__main__':
    main()
