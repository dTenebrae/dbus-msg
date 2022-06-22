#!/usr/bin/env python

import socket
import subprocess

def show_msg(msg):
    subprocess.Popen(['notify-send', msg])
    return

def create_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return sock

client = create_client()
client.bind(("", 37020))
data, addr = client.recvfrom(1024)
msg = data.decode("UTF-8")
show_msg(msg)
