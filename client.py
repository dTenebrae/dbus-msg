#!/usr/bin/env python

import socket
import subprocess
import dbus

def show_msg(msg):
    item              = "org.freedesktop.Notifications"
    path              = "/org/freedesktop/Notifications"
    interface         = "org.freedesktop.Notifications"
    app_name          = "dbus-msg"
    id_num_to_replace = 0
    icon              = "/usr/share/icons/mate/32x32/status/sunny.png"
    title             = "Notification Title"
    text              = msg
    actions_list      = ''
    hint              = ''
    time              = 5000   # Use seconds x 1000

    bus = dbus.SessionBus()
    notif = bus.get_object(item, path)
    notify = dbus.Interface(notif, interface)
    notify.Notify(app_name, id_num_to_replace, icon, title, text, actions_list, hint, time)

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

