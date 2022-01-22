# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread6.py
@time:2021/12/06
"""

"""
有时在多线程状态下，对临界区加锁来避免出现竞态条件(race condition)
线程的调度本质上来说是非确定的，所以在多线程程序中如果不用好锁会让数据被随机得破坏掉
显示得获取锁可以使用
self._value_lock.acquire()
do something
self._value_lock.release()
与此相比使用with可以更加优雅也不会出现acquire但是忘了release的情况
"""

import threading


class SharedCounter:
    """
    A counter object that can be shared by multiple threads
    """

    def __init__(self, initial_value=0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self, delta=1):
        """
        Increment the counter with locking
        :param delta:
        :return:
        """
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        """
        Decrement the counter with locking
        :param delta:
        :return:
        """
        with self._value_lock:
            self._value -= delta


"""
在多线程中，出现死锁的常见原因就是一个线程一次尝试获取多个锁，比如获取到了锁A，但是在获取锁B时发生了阻塞，继而导致了死锁
避免出现死锁的方法是给程序中每一个锁分配一个唯一的数字编号，并且在获取多个锁时只按照编号的升序方式来获取，利用上下文管理器来实现这个机制非常简单
"""

from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()  # 线程的本地存储对象


@contextmanager
def acquire(*locks):
    # sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('lock Order Violation')

    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


"""
这个例子关键之处就在于acquire()函数的第一条语句，根据对象的id来对锁排序，这样无论用户按照什么顺序将锁提供给acquire()函数
它们总是会按照统一的顺序来获取
"""
