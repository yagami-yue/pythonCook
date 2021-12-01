# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:multiprocessing_connection.py
@time:2021/11/15
"""

from multiprocessing.connection import Listener
import traceback
from multiprocessing.context import AuthenticationError


def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print("connection closed")


def echo_server(address, authkey):
    server = Listener(address, authkey=authkey)
    while True:
        try:
            client = server.accept()
            #   deliver_challenge(c, self._authkey)
            #   answer_challenge(c, self._authkey)
            # 一个随机加密的二进制数据发送给客户端
            # 客户端通过约定的秘钥解密后，发送给服务端，服务端通过秘钥解密后验证数据的正确后客户端也发送一次deliver_challenge
            # 双方验证通过后建立一个可信任的连接
            # 和低级的socket不同的是所有消息都是完整无损的，对象通过pickle来进行序列化
            # 如果需要对连接实现更多的底层控制，那么就别使用multiprocessing模块，比如需要支持超时、非阻塞I/O或者任何类似的特性，建议
            # 使用其他库或者直接在socket上来实现这些特性
            echo_client(client)
        except Exception:
            traceback.print_exception()
            traceback.print_exc()


if __name__ == '__main__':
    echo_server(('', 25000), authkey=b'light')
