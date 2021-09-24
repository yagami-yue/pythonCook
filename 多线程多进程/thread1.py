# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread1.py
@time:2021/08/31
"""

from threading import Thread
import time


def my_counter():
    i = 0
    for _ in range(100000000):
        i = i + 1
    return True


def main():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))


if __name__ == '__main__':
    main()
