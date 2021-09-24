# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:test1.py
@time:2021/06/17
"""

# 去除序列中重复元素且保持顺序不变

# items中都是可哈希的元素
import itertools


def dedupe1(items):
    seen = set()
    s = []
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


# items中含有不可哈希的元素
# key方法可以让元素转变成可哈希的，类似与字典变成key，或者(key,value)
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(item)


# s = [2, 3, 9, 1, 5]
# a = dedupe(s)
#
# print(list(a))


# 对切片命名,如果元素可以元素指定，可以通过切片操作替换或者删除一段数据,切片对象有head.start,head.stop,head.step三个属性对应起点，终点，步长
head = slice(0, 5, 2)
foot = slice(5, 10)
# s = 'helloworld'
#
# print(s[head])
# print(s[foot])


# 序列中出现次数最多的元素，使用collections中的Counter类
# Counter(list) 传入一个
s = 'aa bb a b v c aa bb b v h f'
from collections import Counter

counter = Counter(s.split())
print(counter)
# Counter({'aa': 2, 'bb': 2, 'b': 2, 'v': 2, 'a': 1, 'c': 1, 'h': 1, 'f': 1})
# counter.most_common(num) 可以得到最常出现的num个元素，底层使用字典实现
# 可以使用简单的自增 counter[word] += 1,2个counter可以实现加减操作完成次数的加减


# 对列表中的多个字典针对某些字段排序, itemgetter可以接受多个键，多个键用逗号分割
# from operator import itemgetter
# rows = [
#     {'fname': 'Brain', 'lname': 'Jones', 'uid': 1001},
#     {'fname': 'David', 'lname': 'Beazley', 'uid': 1003},
#     {'fname': 'John', 'lname': 'Cleese', 'uid': 1004},
#     {'fname': 'Big', 'lname': 'Jones', 'uid': 1002},
# ]
# rows_by_fname = sorted(rows, key=itemgetter('fname'))
# rows_by_uid = sorted(rows, key=itemgetter('uid'))
# 这种方式可以使用lambda函数来代替，但是性能上还是itemgetter来的快
# rows_by_fname = sorted(rows, key=lambda x:x['fname'])
# from collections import defaultdict
# defaultdict构造时使用的数据结构决定了value的数据结构
# a = defaultdict()
# print(a)
# a['date'] = 11
# print(a)
# b = defaultdict(list)
# print(b)
# b['date'].append(11)
# print(b)
mylist = [1, 4, -5, 10, 7, -8, 2, -3]
a = filter(lambda x: x > 0, mylist)
# filter对象也是一个可迭代的，可以使用list强制转换为list获得所有元素
for item in a:
    print(item)

# itertools.compress()接受一个可迭代对象和一个布尔值序列，能把布尔序列中为True对应的可迭代对象的值筛选出来，该方法也会返回一个迭代器
# 合并多个字典可以从collections import ChainMap，ChainMap接受多个映射转变为一个，并且原来的修改后，ChainMap也会跟着修改，并且
# 如果两个映射有相同的字段，会按照参数顺序显示出Value，修改ChainMap也会作用于第一个映射
