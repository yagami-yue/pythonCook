# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:wav2pcm.py
@time:2022/02/17
"""
import builtins
import struct
import wave

"""
1. wave.open(f, mode)
f为字符串, 当做文件路径，否则当做文件对象
mode = rb or wb

wav文件时标准的riff文件(resource interchange file format)
riff 文件是windows环境下大部分多媒体格式遵循的一种文件格式
音频视频交错格式数据(.avi) 波形格式数据(.wav) 位图格式数据(.rdi) MIDI格式数据(.rmi)
调色板格式(.pal)多媒体电影(.rmn) 动画光标(.ani) 其它RIFF文件（.BND)

CHUNK是组成RIFF文件的基本单元
struct chunk{
    u32 id; /* 块标志 */
    u32 size; /* 块大小 */
    u8 dat[size]; /* 块内容 */
};


chunk块中有且仅有两种类型块：'RIFF'和'LIST'类型可以包含其他块，而其它块仅能含有数据。
'RIFF'和'LIST'类型的chunk结构如下:
structure{
    u32 id; /* 块标志 */
    u32 size; /* 块大小 */
    /*此时的dat = type + restdat */
    u32 type ; /* 类型 */
    u8 restdat[size] /* dat中除type4个字节后剩余的数据*/
};
小于等于512MB的卷，默认簇是512字节
513-1024MB的卷，默认簇是1K
1025-2048MB的卷，默认簇是2K
大于2G的卷，默认簇是4K
"""
with wave.open('output.wav', 'rb') as f:
    print(f.getnchannels())  # 通道数
    print(f.getsampwidth())  # 采样字节长度
    print(f.getframerate())  # 采样频率
    print(f.getnframes())  # 总帧数
    print(f.getcompname())  # 压缩类型
# with builtins.open('小信经理.wav', 'rb') as f:
#     print(f.read(4))    # b'RIFF'
#     var = struct.unpack_from('<' + 'L', f.read(4))  # < 表示小端， > 表示大端 L 表示 unsigned long
#     # 'https://www.cnblogs.com/gala/archive/2011/09/22/2184801.html'
#     print(var, var[0])    # (78406, ) 78406
#     print(f.read(4))      # b'WAVE'
#     print(f.read(4))      # b'fmt '
#     print(f.read(4))  # 小端模式 10 00 00 00
#     print(f.read(2))
#     print(f.read(2))
