import lxml.html
import os
import grequests


def get_html_files(dir):
    #for root, subFolders, files in os.walk("content/"):
    #    for f in files:
    #        with open(os.path.join(root, f), 'r+') as fin:
    #            contents = fin.read()
    pass

def parse_directory(dir):
    pass


def broken_link_exception(file_name, line_number, href):
    raise Exception("Broken link found in file %s on line %s linking to %s" % (file_name, line_number, href))


def get_urls(file_name, html_data):
    '''
    Should return the line # where the
    '''
    urls = []
    html = lxml.html.fromstring(html_data)
    anchor_tags = html.cssselect('a')

    for a in anchor_tags:
        if not 'href' in a.attrib or a.attrib['href'] == '':
            broken_link_exception(file_name, a.sourceline, a)

        url = a.attrib['href']

        if url[0] != '#':
            urls.append((url, file_name, a.sourceline))
            print 'going to check %s' % a.attrib["href"]

    return urls

def check_urls(urls):
    '''
    expected format of urls is tuple (url, file name, source line) i.e. ("google.com", "index.html", 32)
    '''
    requests = (grequests.get(u[0]) for u in urls)

    try:
        result = grequests.map(requests)
    except requests.exceptions.ConnectionError:
        pass

    print result


file_name = "test_data/test.html"
html_data = open("test_data/test.html").read()
urls = get_urls(file_name, html_data)
check_urls(urls)
