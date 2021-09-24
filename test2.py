# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:test2.py
@time:2021/06/17
"""

# def sample():
#     yield 'a'
#     yield 'b'
#     yield 'c'
#     yield 'd'
#
#
# def combine(source, maxsize):
#     parts = []
#     size = 0
#     for part in source:
#         size += len(part)
#         if size > maxsize:
#             yield ''.join(parts)
#             parts = []
#             size = 0
#         parts.append(part)
#     yield ''.join(parts)
#
#
# for part in combine(sample(), 2):
#     print(part)

#
# s = [1, 2, 3, 4, 8]
# for item, num in enumerate(s, 1):
#     print(item, num)


# def count(n):
#     while n < 50:
#         yield n
#         n += 1
#
# import itertools
# c = count(0)
# s = []
# for x in itertools.islice(c, 0, 10):
#     s.append(x)
# print(s)
# for x in itertools.islice(c, 0, None):
#     print(x)
import os
import time
from collections import Iterable
from itertools import chain


def func_time(func):
    def inner(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        end_time = time.time()
        print('函数运行时间为：', end_time - start_time, 's')

    return inner


# @func_time
# def func1():
#     a = list(range(1, 100000))
#     b = list(range(100001, 200000))
#     for i in a + b:
#         i += 1
#
# @func_time
# def func2():
#     a = list(range(1, 100000))
#     b = list(range(100001, 200000))
#     for i in chain(a, b):
#         i += 1
#
# func1()
# func2()
# 函数运行时间为： 0.011968135833740234 s
# 函数运行时间为： 0.010969877243041992 s
# 迭代操作，chain函数要比2个列表合并后效率高点，并且不要求2个iter类型一致，并且内存上使用的较少，因为不用重新创建一个新的列表

#  对可迭代对象做扁平化处理,ignore_types是为了不然字符串和二进制对象也被迭代一个一个输出，后续可以添加其他的类型完成需求
# def flatten(items, ignore_types=(str, bytes)):
#     for i in items:
#         if isinstance(i, Iterable) and not isinstance(i, ignore_types):
#             yield from flatten(i)
#         else:
#             yield i
#
# items = [1, 2, [1, 2]]
# for i in flatten(items):
#     print(i)

# heap.merge()可以把一组有序的序列合并成有序的，返回有序的
# 该函数不会检查序列是否有序只是简单地比较每个序列的首个元素大小，然后把小的发送出去


# iter函数可以接受一个可调用对象和一个值，此时迭代iter(callable, sth)会一直调用callable直到callable返回值=sth
# 一般跟文件IO搭配

# a = 10
# def func1():
#     global a
#     a -= 1
#     print(a)
#     return a
#
#
# for item in iter(func1, 5):
#     print(item)
# s = [1, 5, 3, 5, 9, 4]
# print(sorted(s, key=lambda x, y=2 : x - y if x - y > 0 else y - x))
# import math
#
#
# def distance(p1, p2):
#     x1, y1 = p1
#     x2, y2 = p2
#     return math.hypot(x2 - x1, y2 - y1)
#
#
# points = [(1, 2), (3, 4), (5, 6), (7, 8)]
# y = (0, 0)
# points.sort(key=lambda x, y=y: distance(x, y))
# print(points)

# def output_result(result, log=None):
#     if log is not None:
#         log.debug('Got: %r', result)
#
#
# def add(x, y):
#     return x + y
#
#
# if __name__ == '__main__':
#     import logging
#     from multiprocessing import Pool
#     from functools import partial
#
#     logging.basicConfig(level=logging.DEBUG)
#     log = logging.getLogger('test')
#
#     p = Pool()
#     p.apply_async(add, (3, 4), callback=partial(output_result, log=log))  # 给函数分配一些指定的参数
#     p.close()
#     p.join()