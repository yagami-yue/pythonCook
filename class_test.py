# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:class_test.py
@time:2021/06/24
"""
import time
import threading
import errno
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

body = '''Hello,world! <h1> from the5fire </h1> - from {thread_name}'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Monday, 28 June 2021 09:55:01 GMT',
    'COntent-Type: text/plain; charset=utf-8',
    'Content-Length: {length}\r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    request = b''
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    current_thread = threading.currentThread()
    content_length = len(body.format(thread_name=current_thread.name).encode())
    print(current_thread.name)

    conn.send(response.format(thread_name=current_thread.name, length=content_length).encode())
    conn.close()


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  socket.AF_INET设置服务器服务器之间的网络通信，socket.SOCK_STREAM使用基于TCP的流式socket通信
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(10)  # 设置最大排队数目
    print('http://127.0.0.1:8000')
    serversocket.setblocking(False)

    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise
                continue
            i += 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address), name='thread-%s' % i)
            t.start()
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
