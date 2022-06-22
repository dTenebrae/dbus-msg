#!/usr/bin/env python

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))
data, addr = client.recvfrom(1024)
msg = data.decode("UTF-8")
print(f"recived message: {msg}\tfrom addr {addr}")
