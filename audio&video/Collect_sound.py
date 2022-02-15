# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:Collect_sound.py
@time:2022/02/15
"""
import pyaudio
import wave

p = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
FS = 44100
CHANNELS = 2
CHUNK = 1024
RECORD_SECOND = 5  # 录制秒数

stream = p.open(format=FORMAT, channels=CHANNELS, rate=FS, input=True, frames_per_buffer=CHUNK)
# format=位深, channels=通道数, rate=采样率, input=允许输入, frames_per_buffer=帧缓冲数
print('* recording')

frames = []
num_times = int(RECORD_SECOND * FS / CHUNK)

for i in range(num_times):
    data = stream.read(CHUNK)
    print(data)
    frames.append(data)

print('Done')

# stream.start_stream()
stream.close()
p.terminate()

print(frames)

sample_width = p.get_sample_size(FORMAT)
print(sample_width)

wf = wave.open('output.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(sample_width)  # 位深
wf.setframerate(FS)
wf.writeframes(b''.join(frames))
wf.close()