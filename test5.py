# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:test5.py
@time:2021/08/30
"""

from multiprocessing import Process, Queue
from time import sleep


def sub_task(q, string):
    while True:
        if not q.empty():
            counter = int(q.get())
            while counter < 10:
                print(string, flush=True)
                q.put(str(counter + 1))
                sleep(0.01)
                counter = int(q.get())
            q.put('10')
            break


def main():
    q = Queue()
    q.put('0')
    p1 = Process(target=sub_task, args=(q, 'Ping'))
    p2 = Process(target=sub_task, args=(q, 'Pong'))
    p1.start()
    p2.start()

    # Process(target=sub_task, args=(q, 'Pong')).start()


if __name__ == '__main__':
    main()
    exit(code=0)
