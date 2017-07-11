import urllib.request
import re
import json
import gzip
import zlib

def get_danmaku(url):
    cid = page_parser(url)
    cmt_url = 'http://comment.bilibili.com/{}.xml'.format(cid)
    raw = handle_comp_res(urllib.request.urlopen(cmt_url))
    return str(cid), raw.decode('utf8')

def page_parser(url, charset='utf8'):
    if 'bangumi.bilibili' in url:
        return bangumi_parser(url, charset)
    else:
        return normal_parser(url, charset)

def normal_parser(url, charset):
    import gzip

    aid = re.search(r'/av(\d+)/', url).group(1)
    page = re.search(r'#page=(\d+)', url)
    if page is not None:
        page = page.group(1)

    endpoint = 'http://www.bilibili.com/widget/getPageList?aid={}'.format(aid)
    res = urllib.request.urlopen(endpoint)
    plain = handle_comp_res(res).decode(charset)
    json_data = json.loads(plain)

    if page is not None:
        idx = page - 1
    else:
        idx = 0

    return json_data[idx]['cid']

def bangumi_parser(url, charset):
    ep_id = re.search(r'#(\d+)', url).group(1)
    to_post = ('episode_id=' + ep_id).encode('utf8')
    plain_res = urllib.request.urlopen('http://bangumi.bilibili.com/web_api/get_source', data=to_post)
    json_data = json.loads(plain_res.read().decode('utf8'))
# TODO: check return code
    return json_data['result']['cid']

def handle_comp_res(res):
    data = res.read()
    encoding = res.info().get('Content-Encoding')
    if encoding == 'deflate':
        try:
            return zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            return zlib.decompress(data)
    elif encoding == 'gzip':
        return gzip.decompress(data)
    else:
        return data

