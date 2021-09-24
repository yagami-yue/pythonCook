# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:app.py
@time:2021/06/28
"""


def simple_app(environ, start_response):
    status = '200 ok'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b'hello world! -by light\n']


