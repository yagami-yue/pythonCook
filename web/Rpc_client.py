# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:Rpc_client.py
@time:2021/11/15
"""

import pickle
from multiprocessing.connection import Client


class RPCProxy:
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result

        return do_rpc


if __name__ == '__main__':
    c = Client(('106.15.178.162', 20000), authkey=b'light')
    proxy = RPCProxy(c)
    print(proxy.add(2, 3))
    print(proxy.sub(4, 6))
    c.close()