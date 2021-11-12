# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:restful_server.py
@time:2021/11/12
"""

import time

_hello_resp = '''
<html>
    <head>
        <title>Hello World {name} </title>
    </head>
    <body>
        <h1>Hello {name}</h1>
    </body>
</html>
'''


def hello_world(environ, start_response):
    start_response('200 ok', [('Content-type', 'text/html')])
    params = environ['params']
    print(params, type(params))
    print(environ, type(environ))
    resp = _hello_resp.format(name=params.get('name', 'light'))
    yield resp.encode('utf-8')


_localtime_resp = '''<?xml version="1.0" encoding='utf-8'?>
<time>
    <year>{t.tm_year}</year>
    <month>{t.tm_mon}</month>
    <day>{t.tm_mday}</day>
    <hour>{t.tm_hour}</hour>
    <minute>{t.tm_min}</minute>
    <second>{t.tm_sec}</second>
</time>
'''


def localtime(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')


if __name__ == '__main__':
    from restful_handle_class import PathDispatcher
    from wsgiref.simple_server import make_server

    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)

    # Launch a basic server
    httpd = make_server('', 20000, dispatcher)
    print('server start!!!')
    httpd.serve_forever()
