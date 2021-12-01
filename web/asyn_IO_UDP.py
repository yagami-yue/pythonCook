# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:asyn_IO_UDP.py
@time:2021/11/17
"""

"""
很多python的包是事件驱动或者说是异步I/O的
从根本上说，异步I/O是一种把基本的I/O操作变成事件的技术
比如socket收到数据，使用回调方法来处理并且做出响应
"""


# 定义一个事件处理的类
class EventHandler:
    def fileno(self):
        raise NotImplemented('must implement')

    def wants_to_receive(self):
        return False

    def handle_receive(self):
        pass

    def want_to_send(self):
        return False

    def handle_send(self):
        pass


# 定义一个时间循环

import select


def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        # 事件循环的核心在于select()的调用，它会轮询文件描述符检查它们是否处于活跃状态
        # 在此之前会遍历所有handlers对象是否需要收发数据
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()


# 写两个简单的UDP服务
import socket
import time


# base class
class UDPServer(EventHandler):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True


class UDPTimeServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(1)
        self.sock.sendto(time.ctime().encode('ascii'), addr)


class UDPEchoServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(8192)
        self.sock.sendto(msg, addr)


if __name__ == '__main__':
    handlers = [UDPTimeServer(('', 14000)), UDPEchoServer(('', 15000))]
    event_loop(handlers)
