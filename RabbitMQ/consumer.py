# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:consumer.py
@time:2021/09/26
"""

import pika


# 收到消息后的回调
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 连接服务器
user = pika.PlainCredentials("light", "960912")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=user))
channel = connection.channel()

# rabbitmq消费端仍然使用此方法创建队列。这样做的意思是：若是没有就创建。和发送端道理道理。目的是为了保证队列一定会有
channel.queue_declare(queue='test232')

channel.basic_consume(queue='test232', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
connection.close()