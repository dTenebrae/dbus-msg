#!/usr/bin/env python

import socket
import dbus
import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser(description="Client side of message broadcasting app")

    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=37020,
        help="Port to use. Default is 37020"
    )
    parser.add_argument(
        '-t',
        '--time',
        type=int,
        default=10,
        help="Time(sec) to sleep between sending another message. Default is 10"
    )

    return parser.parse_args()


def show_msg(msg):
    # TODO try except
    msg = msg.decode("UTF-8")

    header, body = msg.split("<DEL>")

    dbus_attr = {
        "item": "org.freedesktop.Notifications",
        "path": "/org/freedesktop/Notifications",
        "interface": "org.freedesktop.Notifications",
        "app-name": "dbus-msg",
        "id-num-to-replace": 0,
        "icon": "/usr/share/icons/mate/32x32/status/sunny.png",
        "title": header,
        "text": body,
        "actions-list": "",
        "hint": "",
        "time": 5000  # msec
    }

    bus = dbus.SessionBus()
    notif = bus.get_object(dbus_attr["item"],
                           dbus_attr["path"])

    notify = dbus.Interface(notif,
                            dbus_attr["interface"])

    notify.Notify(dbus_attr["app-name"],
                  dbus_attr["id-num-to-replace"],
                  dbus_attr["icon"],
                  dbus_attr["title"],
                  dbus_attr["text"],
                  dbus_attr["actions-list"],
                  dbus_attr["hint"],
                  dbus_attr["time"])


def create_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return sock


if __name__ == "__main__":
    args = parse_args()
    # на какой порт посылаем
    port = args.port
    # пауза между получением сообщений
    t = args.time

    client = create_client()
    client.bind(("", port))
    while True:
        data, addr = client.recvfrom(1024)
        show_msg(data)
        time.sleep(t)
