# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:struct_test.py
@time:2021/11/16
"""
import struct
import binascii

values = (1, bytes('abcsdj', encoding='utf-8'), 2.7)

packed_data = struct.pack('i6sf', *values)
unpacked_data = struct.unpack('i6sf', packed_data)

print(values)
# print(s)
print(packed_data)
print(unpacked_data)
print(unpacked_data[1].decode('utf-8'))