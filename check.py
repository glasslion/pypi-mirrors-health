from datetime import datetime
import requests


def check_mirror(url):
    r = requests.get(url)
    r.raise_for_status()
    timestamp = r.text.strip('\n')
    last_modified = datetime.strptime(timestamp, '%Y%m%dT%H:%M:%S')
    now = datetime.utcnow()
    assert (now-last_modified).days < 1





check_mirror('https://mirrors.ustc.edu.cn/pypi/web/last-modified')