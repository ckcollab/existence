import lxml.html
import os
import platform
import sys
import urllib2

from progressbar import ProgressBar, SimpleProgress
from threading import Thread


ROOT_DIRECTORY = ''
URL_CACHE = []
BROKEN_URLS = []
SHOW_PROGRESS_BAR = True


def directory_get_urls(directory):
    urls = []

    for root, subFolders, files in os.walk(directory):
        for f in files:
            if f.endswith(".html"):
                full_path = os.path.join(root, f)

                with open(full_path, 'r+') as fin:
                    new_urls = parse_html_urls(full_path, fin.read())

                    if new_urls:
                        urls = urls + new_urls

    return urls


def parse_html_urls(file_name, html_data):
    '''
    Returns a list of tuples in the form (url, file_name, line_number)
    '''
    try:
        urls = []
        html = lxml.html.fromstring(html_data)
        anchor_tags = html.cssselect('a')

        for a in anchor_tags:
            # A link was started but not finished, href with nothing set!
            if not 'href' in a.attrib or a.attrib['href'] == '':
                BROKEN_URLS.append(('None', file_name, a.sourceline))

            url = clean_url(a.attrib['href'])

            if is_valid_url(url):
                if not any(url == u for u in URL_CACHE):
                    urls.append((url, file_name, a.sourceline))
                    URL_CACHE.append(url)

        return urls

    except SyntaxError:
        pass


def is_valid_url(url):
    if url.startswith("#"):
        return False

    if url.startswith("mailto"):
        return False

    return True


def clean_url(url):
    if platform.system() == "Windows":
        if url.startswith("C:\\"):
            url = url.replace("C:\\", "file:///C:/")

    return url


def async_check_url(url, file_name, line_number):
    try:
        urllib2.urlopen(url)
    except urllib2.URLError:
        BROKEN_URLS.append((url, file_name, line_number))


def check_urls(urls):
    '''
    expected format of urls is list of tuples (url, file name, source line) i.e. ("google.com", "index.html", 32)
    '''
    threads = list()
    progress_bar = None
    progress_counter = 0

    if SHOW_PROGRESS_BAR and len(urls) > 0:
        widgets = [SimpleProgress()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(urls)).start()

    for u in urls:
        t = Thread(target=async_check_url, args=(u[0], u[1], u[2]))
        t.start()
        threads.append(t)

    for thread in threads:
        if SHOW_PROGRESS_BAR and len(urls) > 0:
            progress_counter = progress_counter + 1
            progress_bar.update(progress_counter)

        thread.join()

    if SHOW_PROGRESS_BAR and len(urls) > 0:
        progress_bar.finish()


def scan_directory_for_bad_urls(directory):
    urls = directory_get_urls(directory)
    check_urls(urls)

    return BROKEN_URLS


def main():
    if len(sys.argv) == 1:
        print 'Existence requires a directory as an argument!'
        exit(-1)

    ROOT_DIRECTORY = sys.argv[1]

    if not os.path.exists(ROOT_DIRECTORY):
        print 'Existence cannot find the directory %s' % ROOT_DIRECTORY
        exit(-1)

    if not os.path.isdir(ROOT_DIRECTORY):
        print 'Existence requires a directory as an argument!'
        exit(-1)

    print "Checking links..."

    scan_directory_for_bad_urls(ROOT_DIRECTORY)

    if len(BROKEN_URLS) > 0:
        for url in BROKEN_URLS:
            print "Broken link found in file %s on line %s linking to %s" % (url[1], url[2], url[0])

        exit(-1)
    else:
        print "All of your links exist!"


#if __name__ == '__main__':
#    main()
