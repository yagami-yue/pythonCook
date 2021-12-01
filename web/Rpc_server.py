# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:Rpc_server.py
@time:2021/11/15
"""

from multiprocessing.connection import Listener
from threading import Thread
from Rpc_handle import RPCHandler


def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client, address))
        t.daemon = True
        t.start()


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)

rpc_server(handler, ('', 20000), authkey=b'light')
