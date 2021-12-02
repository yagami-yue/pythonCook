# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:publish.py.py
@time:2021/09/26
"""
import pika
user = pika.PlainCredentials("light", "960912")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=user))
channel = connection.channel()

channel.queue_declare(queue='test232')
channel.basic_publish(exchange='', routing_key='test232', body='rabbitmq test2')
print('{} sent hello world!')
connection.close()


