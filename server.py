#!/usr/bin/env python

import socket
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Server side of message broadcasting app")
    parser.add_argument(
        '-t',
        '--text',
        type=str,
        default="some message",
        help="Message to send over LAN"
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
    msg = args.text.encode("UTF-8")
    server = create_server()
    while True:
        server.sendto(msg, ("localhost", 37020))
        time.sleep(1)
