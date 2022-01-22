# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread7.py
@time:2021/12/06
"""
from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM
import threading
from threading import Thread
from queue import Queue

"""
保持线程专有状态，而且需要让状态对其他线程不可见
可以使用threading.local()来创建一个线程本地存储对象，在这个对象上来保存和读取的属性只对当前运行的线程可见
大部分程序创建和操作线程专有状态都不会有什么问题，但是万一出现问题，通常是因为多个线程都使用了同一个对象
而该对象使用或者操作了某种系统资源，比如socket或者文件，不能让一个单独的socket对象被所有线程共享，通过线程专有存储来解决问题
"""


class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, 'sock'):
            raise RuntimeError("Already connected")
        self.local.sock = socket(self.family, self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.local.sock.close()
        del self.local.sock


"""
一般来说不要编写那种允许线程数目无线增长的程序

"""

# def echo_client(sock, client_addr):
#     """
#     Handle a client connection
#     :param sock: sock
#     :param client_addr: ip_addr
#     :return:
#     """
#     print('Got connect from', client_addr)
#     while True:
#         msg = sock.recv(65536)
#         if not msg:
#             break
#         sock.sendall(msg)
#     print('Client closed connection')
#     sock.close()
#
#
# def echo_server(addr):
#     pool = ThreadPoolExecutor(128)
#     sock = socket(AF_INET, SOCK_STREAM)
#     sock.bind(addr)
#     sock.listen(5)
#     while True:
#         client_sock, client_addr = sock.accept()
#         pool.submit(echo_client, client_sock, client_addr)


# echo_server(('', 15000))
"""
想要手动创建自己的线程池，使用Queue是足够简单的
下面对上述的代码做了一定修改
"""


def echo_client(q):
    """
    Handle a client connection
    :param q:
    :return:
    """
    sock, client_addr = q.get()
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()


def echo_server(addr, net_workers):
    # Launch the client workers
    q = Queue()
    for n in range(net_workers):
        t = Thread(target=echo_client, args=(q,))
        t.daemon = True
        t.start()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        q.put((client_sock, client_addr))


echo_server()

"""
一般创建线程池都是使用ThreadPoolExecutor而不是像上面一样手动创建
因为通过.submit()可以很方便的传递需要执行的方法和参数，并且拿到返回的结果
尽管限制了线程池的大小，但是无法阻止恶意用户对服务器发起大量的请求，从而导致服务器上创建了大量的线程，耗尽了系统资源而崩溃
但是在现代的系统上创建拥有几千个线程的线程池是不会有什么问题的，让一千个线程等待工作也不会对其他部分产生性能上的影响
但是这么多线程在同一时间被唤醒开始使用CPU就是比较大的问题(惊群现象)，尤其在解放GIL的情况下,一般来说线程池只适用于IO密集型的任务
创建大型的线程池需要考虑的一个方面就是内存使用，如果创建了2k个线程，系统限制python进程占用了9GB的虚拟内存，
但是实际上只有其中的一小部分映射到了物理内存上，只使用了70MB的物理内存，如果需要考虑虚拟内存的大小可以使用
thread.stack_size(num)
num最小为32768字节(32MB)，通常会限制这个值为系统内存页面大小的整数倍(一般为4KB)
"""
