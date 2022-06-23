#!/usr/bin/env python

import socket
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Server side of message broadcasting app")

    parser.add_argument(
        '-s',
        '--string',
        type=str,
        default="Кушать подано",
        help="Message to send over LAN"
    )
    parser.add_argument(
        '-H',
        '--header',
        type=str,
        default="from server",
        help="Header of popup window on client side"
    )
    parser.add_argument(
        '-t',
        '--time',
        type=int,
        default=1,
        help="Time(sec) to sleep between sending another message. Default is 1"
    )
    parser.add_argument(
        '-n',
        '--number',
        type=int,
        default=9999,
        help="Number of messages you want to send. Default is 9999"
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=9999,
        help="Port to use. Default is 9999"
    )

    return parser.parse_args()


def create_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.2)
    return sock


if __name__ == "__main__":
    args = parse_args()

    # парсим аргументы запуска сервера
    msg = (args.header + "<DEL>" + args.string).encode("UTF-8")
    t = args.time
    n = args.number
    port = args.port

    # создаем сокет
    server = create_server()

    # кидаем в пространство наше сообщение с интервалом time
    i = 0
    while i <= n:
        server.sendto(msg, ("localhost", port))
        time.sleep(t)
        i += 1
