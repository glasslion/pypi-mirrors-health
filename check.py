from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class Mirror:
    name: str
    location: str
    status: bool  = False
    last_modified: str  = ''


MIRROES = [Mirror(*args) for args in (
    ('豆瓣', 'http://pypi.doubanio.com/simple',),
    ('阿里云', 'http://mirrors.aliyun.com/pypi/simple',),
    ('清华', 'https://pypi.tuna.tsinghua.edu.cn/simple',),
    ('中科大', 'https://mirrors.ustc.edu.cn/pypi/web/simple',),
)]


def check_mirror(location):
    status_url = location.replace('/simple', '/last-modified')
    try:
        timestamp = ''
        r = requests.get(status_url)
        r.raise_for_status()
        timestamp = r.text.strip('\n')
        last_modified = datetime.strptime(timestamp, '%Y%m%dT%H:%M:%S')
        now = datetime.utcnow()
        assert (now-last_modified).days < 1
        return (True, timestamp)
    except:
        return (False, timestamp)


def get_badge(status):
    if status:
        return '![staus OK](https://img.shields.io/badge/staus-OK-brightgreen.svg?style=for-the-badge)'
    else:
        return '![staus fail](https://img.shields.io/badge/staus-fail-red.svg?style=for-the-badge)'


def render_markdown_table(mirrors):
    rows = [['PyPI Mirror', 'Location', 'Status', 'Last Modified']]
    rows.append(['---']*4)
    for m in mirrors:
        rows.append([m.name, m.location, get_badge(m.status), m.last_modified])
    text = ''
    for row in rows:
        text += '| ' + ' | '.join(row) + ' |\n'
    return text



def main():
    for mirror in MIRROES:
        mirror.status, mirror.last_modified = check_mirror(mirror.location)
    table = render_markdown_table(MIRROES)
    readme = """PyPI Mirrors Health Checker
===========================
"""
    readme += '\n' + table
    print(readme)


if __name__ == '__main__':
    main()