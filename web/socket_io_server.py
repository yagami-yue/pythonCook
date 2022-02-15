# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:socket_io_server.py
@time:2022/02/11
"""
import eventlet
import socketio


"""
对于基于 asyncio 的服务器，socketio.AsyncServer 类提供相同的功能，但采用协程友好的格式。
如果需要，socketio.ASGIApp 类可以将服务器转换为标准的 ASGI 应用程序
"""
sio = socketio.Server()

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

# sio = socketio.AsyncServer()
# app = socketio.ASGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
