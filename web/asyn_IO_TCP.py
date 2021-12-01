# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:asyn_IO_TCP.py
@time:2021/11/17
"""
import socket

from asyn_IO_UDP import EventHandler, event_loop

"""
相比UDP,TCP服务器就要复杂一点，因为每一个客户端都需要涉及并产生一个新的处理对象
一些参数说明:
 SOL_SOCKET SO_REUSEADDR 允许重用本地地址和端口
 SOL_SOCKET SO_KEPALIVE 保持连接
 SOL_SOCKET SO_LINGER 延迟关闭连接
 SOL_SOCKET SO_BROADCAST 允许发送广播数据
 SOL_SOCKET SO_OOBINLINE 带外数据放入正常数据流
 SOL_SOCKET SO_SNDBUF 发送缓冲区大小
 SOL_SOCKET SO_RCVBUF 接收缓冲区大小
 SOL_SOCKET SO_TYPE 获得套接字类型
 SOL_SOCKET SO_ERROR 获得套接字错误
 SOL_SOCKET SO_DEBUG 允许调试
 SOL_SOCKET SO_RCVLOWAT 接收缓冲区下限
 SOL_SOCKET SO_SNDLOWAT 发送缓冲区下限
 SOL_SOCKET SO_RCVTIMEO 接收超时
 SOL_SOCKET SO_SNDTIMEO 发送超时
 SOL_SOCKET SO_BSDCOMPAT 与BSD系统兼容
 IPPROTO_IP IP_HDRINCL　　在数据包中包含IP首部
 IPPROTO_IP IP_OPTINOS　　　　IP首部选项　
 IPPROTO_IP IP_TOS　　　　　服务类型
 IPPROTO_IP IP_TTL　　　　　生存时间
 IPPRO_TCP TCP_MAXSEG　　TCP最大数据段的大小
 IPPRO_TCP TCP_NODELAY　　不使用Nagle算法
"""


class TCPServer(EventHandler):
    def __init__(self, address, client_handler, handler_list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind(address)
        self.sock.listen(1)
        self.client_handler = client_handler
        self.handler_list = handler_list

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

    def want_to_send(self):
        return True

    def handle_receive(self):
        client, addr = self.sock.accept()
        self.handler_list.append(self.client_handler(client, self.handler_list))


class TCPClient(EventHandler):
    def __init__(self, sock, handler_list):
        self.sock = sock
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        return self.sock.fileno()

    def close(self):
        self.sock.close()
        self.handler_list.remove(self)

    def want_to_send(self):
        return True if self.outgoing else False

    def handle_send(self):
        nsent = self.sock.send(self.outgoing)
        self.outgoing = self.outgoing[nsent:]


class TCPEchoClient(TCPClient):
    def wants_to_receive(self):
        return True

    def handle_receive(self):
        data = self.sock.recv(8192)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)


if __name__ == '__main__':
    handlers = [TCPServer(('', 16000), TCPEchoClient, [])]
    event_loop(handlers)
