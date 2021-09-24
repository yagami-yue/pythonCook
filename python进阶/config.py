# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:config.py
@time:2021/09/14
"""
from urllib.parse import urljoin


def read_config_file(path):
    """Reads all UPPERCASE variables defined in the given module file path."""
    from runpy import run_path
    settings = run_path(path)
    return dict([(k, v)
                 for k, v in settings.items()
                 if k.upper() == k])


if __name__ == '__main__':

    status_center_url = 'https://test-statuscenter.xmov.ai/'
    url = urljoin(status_center_url, 'room_id/')
    print(url)
