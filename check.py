from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class Mirror:
    name: str
    location: str
    status: bool  = False
    last_modified: datetime  = None


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
        return (True, last_modified)
    except:
        return (False, last_modified)


def get_badge(status):
    if status:
        return '![staus OK](https://img.shields.io/badge/staus-OK-brightgreen.svg?style=for-the-badge)'
    else:
        return '![staus fail](https://img.shields.io/badge/staus-fail-red.svg?style=for-the-badge)'


def render_markdown_table(mirrors):
    rows = [['PyPI Mirror', 'Location', 'Status', '上次同步时间']]
    rows.append(['---']*4)
    for m in mirrors:
        rows.append([
            m.name, m.location, get_badge(m.status),
            m.last_modified.strftime('%Y-%m-%d %H:%M:%S')
        ])
    text = ''
    for row in rows:
        text += '| ' + ' | '.join(row) + ' |\n'
    return text


def show_outages(mirrors):
    now = datetime.utcnow()
    snow = now.strftime('%Y-%m-%d')
    with open('./outages.txt', 'a' ) as f:
        for m in MIRROES:
            if not m.status:
                days = (now - m.last_modified).days
                f.write(f'{snow}   {m.location} DOWN {days}days\n')


def main():
    for mirror in MIRROES:
        mirror.status, mirror.last_modified = check_mirror(mirror.location)
    table = render_markdown_table(MIRROES)
    readme = """PyPI Mirrors Health Status
===========================

## 缘起
由于众所周知的原因， 国内访问 PyPI 官方源的速度很不稳定。 尽管有众多的第三方源，但这些第三方源的稳定性欠佳， 都曾经出现长时间未和官方源同步的问题。 本项目会每天检查各第三方源的同步状态， 便于大家评估和选择靠谱的源。
如果想知道各个源同步问题的历史记录，可以查看项目里的 outages.txt 文件
"""
    readme += '\n' + table
    with open('./README.md', 'w' ) as f:
        f.write(readme)
    show_outages(MIRROES)


if __name__ == '__main__':
    main()
