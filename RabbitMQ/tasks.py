# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:tasks.py
@time:2021/09/26
"""
import celery.result
from celery import Celery
import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('', broker='amqp://guest@localhost//')
# celery.result.AsyncResult

@app.task
def add(x, y):
    return x + y
