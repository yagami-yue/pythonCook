# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:test4.py
@time:2021/08/29
"""
import sys

f = ["A", "B", "C", [1, 2, 3, 4, 5, 6]]
f2 = [1, ]
f3 = ["", ["A", "B", "C", [1, 2, 3, 4, 5, 6]]]
f4 = []
f5 = True
f6 = list()
# print(sys.getsizeof(f), sys.getsizeof(f2), sys.getsizeof(f3), sys.getsizeof(f4))
# print(sys.getsizeof(f3[0]), sys.getsizeof(f5), sys.getsizeof(f6))


import time

from time import time, localtime, sleep


class Clock(object):
    """数字时钟"""

    def __init__(self, hour=0, minute=0, second=0):
        self._hour = hour
        self._minute = minute
        self._second = second

    @classmethod
    def now(cls):
        ctime = localtime(time())
        return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)

    def run(self):
        """走字"""
        self._second += 1
        if self._second == 60:
            self._second = 0
            self._minute += 1
            if self._minute == 60:
                self._minute = 0
                self._hour += 1
                if self._hour == 24:
                    self._hour = 0

    def show(self):
        """显示时间"""
        return '%02d:%02d:%02d' % \
               (self._hour, self._minute, self._second)


def main():
    # 通过类方法创建对象并获取系统时间
    clock = Clock.now()
    while True:
        print(clock.show())
        sleep(1)
        clock.run()


if __name__ == '__main__':
    main()
