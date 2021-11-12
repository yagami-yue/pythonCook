# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:tcp_client.py
@time:2021/09/02
"""
from socket import socket


def main():
    # 1.创建套接字对象默认使用IPv4和TCP协议
    client = socket()
    client.connect(('192.168.91.25', 30000))
    # 2.连接到服务器(需要指定IP地址和端口)
    while True:

        msg = input("请输入msg:")

        client.send(bytes(msg, encoding="utf-8"))
        # 3.从服务器接收数据es
        print(client.recv(1024).decode('utf-8'))
        if msg == "":
            break

    client.close()
    print("connect close")


if __name__ == '__main__':
    main()