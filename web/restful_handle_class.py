# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:restful_handle_class.py
@time:2021/11/12
"""

import cgi


def notfound_404(environ, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']


class PathDispatcher:
    def __init__(self):
        self.path_map = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = self.path_map.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.path_map[method.lower(), path] = function
        return function
