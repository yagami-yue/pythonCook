# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:timeclock.py
@time:2021/08/05
"""
import time
from functools import wraps


def timeclock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        with open('time.txt', 'a') as f:
            f.write('{} use time:{}\n'.format(func.__name__, end-start))
        return result
    return wrapper

@timeclock
def countdown(n):
    while n > 0:
        n -= 1

if __name__ == '__main__':
    # countdown(1000)
    countdown(1000000)
    print('success')
