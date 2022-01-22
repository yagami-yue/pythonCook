# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread5.py
@time:2021/12/06
"""

"""
# 多个线程之间实现安全的通信或者交换数据
# 解决方案: 使用queue中的Queue，被所有线程共享,使用put,get来实现添加和移除元素
# 当使用这种队列的时候，如何对消费者和生产者做一个同步，一般使用一个特殊的终止的信号量
# 当生产者停止生产，就把信号量put进队列，而当消费者拿到这个信号量停止消费，并且再丢一个终止信号量进队列，来让其他消费者停止消费
"""
import time
from queue import Queue
from threading import Thread, Event

# A thread that produces data

# def producer(out_q):
#     while True:
#         data = 0
#         # produce some data
#         out_q.put(data)
#
#
# def consumer(in_q):
#     while True:
#         data = in_q.get()
#         # process the data


"""
通过队列来实现线程间通信是一种单方向且不确定的过程。一般来说，我们无法得知接收线程(消费者)何时会实际接收到消息并且开始工作
但是，Queue对象的确提供了一些基本完成功能
Queue提供了2个方法来同步，join方法会阻塞主程序直到Queue的task_done方法被触发，相当于get次数=task_done次数才能取消阻塞
"""

# def producer(out_q, n=10):
#     while n >= 0:
#         print("producer data:", n)
#         out_q.put(n)
#         n -= 1
#
#
# def consumer(in_q):
#     while True:
#         data = in_q.get()
#         if data == 0:
#             in_q.task_done()
#             break
#         print("process data to:", data * 10)
#         in_q.task_done()


#

"""
当消费者线程已经处理了某项特定的数据，而生产者线程需要立刻感知的话，那么就应该在队列里把一个Event对象绑定在一起，这样生产者就可以监视消费过程
"""


# example
def producer(out_q, n=10):
    while n > 0:
        evt = Event()
        out_q.put((n, evt))
        evt.wait()
        print('data {} process success'.format(n))
        n -= 1


def consumer(in_q):
    while True:
        data, evt = in_q.get()
        if data == 1:
            break
        time.sleep(5)
        # process data
        print("data processing{}".format(data))
        evt.set()
        # set会把evt.wait()唤醒继续向下执行


q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q, 20))
t1.start()
t2.start()

"""
在线程中使用queue，把数据放入队列不会产生该数据的拷贝，因此通信过程实际上涉及在不同的线程间传递对象的引用
如果需要共享状态，那就传递不可变的数据结构，要么就对数据做深拷贝
Queue对象在初始化可以传递一个参数来限制大小
如果生产者消费者对数据的生产消费速度有很大差异，就需要加一个队列长度，但是当队列满将程序阻塞也会产生很多以外的连锁反应，可能会导致死锁或者
运行效率太差的情况，所以在线程间通信的控制流是一个实际上很困难的问题，如果发现试图去调整队列大小来修正问题，说明程序设计的不够健壮或者存在固有拓展问题
get、put方法都有非阻塞和超时机制
-------------------------
try:
    data = q.get(block=false)
except queue.Empty:
    pass
-------------------------
try:
    q.put(item, block=False)
except queue.Full:
    pass
-------------------------
这两种机制都可以用来避免在特定的队列上操作无期限的阻塞下去
queue还有一些方法来检查queue的状态
q.qsize()
q.full()
q.empty()
但是不能依赖这些方法，多线程情况下，可能刚调用empty()，另一个线程就加入了一个元素
"""
