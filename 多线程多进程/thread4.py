# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread4.py
@time:2021/12/03
"""

# 如果打算一遍又一遍重复通知某个事件，那最好使用Condition对象来处理

import threading
import time


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        """
        run the timer and notify waiting threads after each interval
        :return: None
        """
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag = 1
                self._cv.notify_all()

    def wait_for_tick(self):
        """
        wait for the next tick of the timer
        :return: None
        """
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()
