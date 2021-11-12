# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:UDP_timeserver.py
@time:2021/11/12
"""

from socketserver import BaseRequestHandler, UDPServer
import time


class TimeHandler(BaseRequestHandler):
    def handle(self):
        print("Got connection from {}".format(self.client_address))
        msg, sock = self.request
        resp = time.time()
        sock.sendto(resp.encode("ascii"), self.client_address)


if __name__ == '__main__':
    serv = UDPServer(('', 20000), TimeHandler)
    serv.serve_forever()


