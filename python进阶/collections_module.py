# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:collections_module.py
@time:2021/09/03
"""

# namedtuple：命令元组，它是一个类工厂，接受类型的名称和属性列表来创建一个类。
# deque：双端队列，是列表的替代实现。Python中的列表底层是基于数组来实现的，而deque底层是双向链表，因此当你需要在头尾添加和删除元素是，deque会表现出更好的性能，渐近时间复杂度为$O(1)$。
# Counter：dict的子类，键是元素，值是元素的计数，它的most_common()方法可以帮助我们获取出现频率最高的元素。Counter和dict的继承关系我认为是值得商榷的，按照CARP原则，Counter跟dict的关系应该设计为关联关系更为合理。
# OrderedDict：dict的子类，它记录了键值对插入的顺序，看起来既有字典的行为，也有链表的行为。
# defaultdict：类似于字典类型，但是可以通过默认的工厂函数来获得键对应的默认值，相比字典中的setdefault()方法，这种做法更加高效。
"""
找出序列中出现次数最多的元素
python 中的字典在发生哈希冲突使用的是开放寻址法，但是hashmap采用了链接法
开放寻址法，在发生哈希冲突时把冲突的键放在下一个空槽内
链接法，在发生哈希冲突用一个指针连接冲突的键
采用开放定址法处理散列表的冲突时，其平均查找长度高于链接法处理冲突
链接法其中优点有： 
1、链接法处理冲突简单，且无堆积现象，即非同义词决不会发生冲突，因此平均查找长度较短；
2、由于链接法中各链表上的结点空间是动态申请的，故它更适合于造表前无法确定表长的情况。
开放寻址法不用指针，潜在地节约了空间，用这些空间可存放更多的槽，从而潜在地减少了冲突，提升了速度
但是在第一个键被删除时，需要对后面有冲突的键做迁移处理，不然会找不到冲突的数据，需要额外的处理时间

"""
from collections import Counter

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around',
    'the', 'eyes', "don't", 'look', 'around', 'the', 'eyes',
    'look', 'into', 'my', 'eyes', "you're", 'under'
]
counter = Counter(words)
print(counter.most_common(3))
