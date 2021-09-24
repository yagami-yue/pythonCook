# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:await.py
@time:2021/09/17
"""
import asyncio
import random
from time import sleep


class Potato:
    @classmethod
    def make(cls, num, *args, **kws):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls, *args, **kws))
        return potatos


all_potatos = Potato.make(5)


async def ask_for_potato():
    await asyncio.sleep(random.random())
    all_potatos.extend(Potato.make(random.randint(1, 10)))


async def take_potatos(num):
    count = 0
    while True:
        if len(all_potatos) == 0:
            await ask_for_potato()
        potato = all_potatos.pop()
        yield potato
        count += 1
        if count == num:
            break


async def buy_potatos():
    bucket = []
    async for p in take_potatos(50):
        bucket.append(p)
        print(f'Got potato {id(p)}...')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(buy_potatos())
    loop.close()