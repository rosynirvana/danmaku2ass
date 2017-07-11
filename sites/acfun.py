import urllib.request
import re

def get_danmaku(url):
    vid = page_parser(url)
    raw = urllib.request.urlopen('http://danmu.aixifan.com/V2/' + vid).read()
    return vid, raw.decode('utf8')

def page_parser(url, charset='utf8'):
    page_content = urllib.request.urlopen(url).read().decode(charset)
    patt = r'data-vid="(\d+)"'
    return re.search(patt, page_content).group(1)
