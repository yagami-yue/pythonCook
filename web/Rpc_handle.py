# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:Rpc_handle.py
@time:2021/11/15
"""
# 如何在socket、multiprocessing.connection或者ZeroMQ这样的消息传递层上实现简单的RPC

import pickle
import logging
from datetime import datetime
log = logging.getLogger('test.log')


class RPCHandler:

    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection, address):
        try:
            while True:
                # receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                try:
                    log.info('{} recv from {} function:{}'.format(datetime.now(), address, func_name))
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))

        except EOFError:
            pass
