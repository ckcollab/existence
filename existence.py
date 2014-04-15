import lxml.html
import os
import sys
import urllib2

from threading import Thread


ROOT_DIRECTORY = ''
URL_CACHE = {}


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


def bad_url_exception_handler(request, exception):
    broken_link_exception(request.url, request.kwargs["file_name"], request.kwargs["line_number"])


def broken_link_exception(url, file_name, line_number):
    raise Exception("Broken link found in file %s on line %s linking to %s" % (file_name, line_number, url))


def is_url_remote(url):
    if url.startswith("http://") or url.startswith("https://"):
        return True

    return False


def parse_html_urls(file_name, html_data):
    '''
    Should return the line # where the
    '''
    try:
        urls = []
        html = lxml.html.fromstring(html_data)
        anchor_tags = html.cssselect('a')

        for a in anchor_tags:
            # A link was started but not finished, href with nothing set!
            if not 'href' in a.attrib or a.attrib['href'] == '':
                broken_link_exception(file_name, a.sourceline, 'NOTHING!')

            url = a.attrib['href']

            if is_url_remote(url):
                if not any(url == u[0] for u in urls):
                    urls.append((url, file_name, a.sourceline))

        return urls

    except SyntaxError:
        pass


def async_check_url(url, file_name, line_number):
    response = urllib2.urlopen(url)

    print "Checking: %s" % url

    if response.code != 200:
        broken_link_exception(url, file_name, line_number)


def check_urls(urls):
    '''
    expected format of urls is tuple (url, file name, source line) i.e. ("google.com", "index.html", 32)
    '''
    threads = list()

    for u in urls:
        t = Thread(target=async_check_url, args=(u[0], u[1], u[2]))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def check_directory(directory):
    urls = directory_get_urls(directory)
    check_urls(urls)


if __name__ == '__main__':
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

    check_directory(ROOT_DIRECTORY)

    print "All of your links exist!"
