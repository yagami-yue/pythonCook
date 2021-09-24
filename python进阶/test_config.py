# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:test_config.py
@time:2021/09/14
"""
import os
import socket
import requests
from urllib.parse import urljoin


DEBUG = False
OFFLINE = False

PORT0 = 5000  # ttsa_backend
PORT1 = 8080  # cirrus
PORT2 = 8124  # ue pixelstreaming
PORT3 = 5558  # ue audio
PORT4 = 6558  # ue face animation
PORT5 = 50060 # ue grpc
PORT6 = 50160 # wtrr grpc

LOCAL_IP = '192.168.88.1'
STATUSCENTER_URL = "http://test-statuscenter.xmov.ai/"
JANUS_SERVER_URL = 'http://test-janus.xmov.ai/janus'

# ip and port
host_mode = os.environ.get('DOCKER_HOST_MODE', False)
if host_mode:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
else:  # bridge mode
    local_ip = LOCAL_IP

ttsa_port = os.environ.get('PORT0', PORT0)
janus_cirrus_port = os.environ.get('PORT1', PORT1)
ue_pixelstreaming_port = os.environ.get('PORT2', PORT2)
ue_grpc_port = os.environ.get('PORT5', PORT5)
wtrr_grpc_port = os.environ.get('PORT6', PORT6)


UE4_SERVER_INFO = "http://%s:%s"% (local_ip, janus_cirrus_port)
TTSA_SERVER_INFO = "http://%s:%s"% (local_ip, ttsa_port)
UE4_GRPC_SERVER_INFO = "%s:%s"% (local_ip, ue_grpc_port)
WTRR_GRPC_SERVER_INFO = "%s:%s"% (local_ip, wtrr_grpc_port)
EXCLUDE_ICE_IPS = []

MEDIA_SOURCE_TYPE = 'ue426_h264_stream'
UE4_HOST = local_ip
UE4_PORT = ue_pixelstreaming_port


# janus cirrus settings
WEBRTC_TYPE = 'janus'
JANUS_CIRRUS_SOCKETIO_URL = UE4_SERVER_INFO


# statuscenter settings
STATUSCENTER_URL = os.environ.get("STATUSCENTER_URL", STATUSCENTER_URL)


# room_id settings
def get_room_id():
    url = urljoin(STATUSCENTER_URL, 'room_id/')
    headers = {"Content-type": "application/json"}
    data = {'room_ip': local_ip, 'room_port': janus_cirrus_port}
    res = requests.post(url, json=data, headers=headers)
    res_data = res.json()
    return res_data['data']['room_id']

ROOM_ID = get_room_id()
