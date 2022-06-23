#!/usr/bin/env python

import socket
import time
import argparse
import ipaddress


def ip_range(start, end):
    """
    Генерирует список ip адресов в диапазоне start-end
    start, end могут быть int или str (в формате "x.x.x.x")
    """
    return [
        ipaddress.ip_address(i).exploded
        for i in range(int(ipaddress.ip_address(start)),
                       int(ipaddress.ip_address(end)))
    ]


def parse_args():
    parser = argparse.ArgumentParser(description="Server side of message broadcasting app")

    parser.add_argument(
        '-m',
        '--message',
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
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        default="",
        help="Path to file with ip addresses. Default is empty string, which leads to localhost"
    )
    parser.add_argument(
        '-r',
        '--range',
        type=str,
        default="",
        help="Range of ip addresses. Example: 192.168.1.1-192.168.1.255. Default is none"
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

    # парсим аргументы запуска сервера.

    # сообщение для отправки. Вставляем делиметр для последующего разбора на запчасти на стороне клиента
    msg = (args.header + "<DEL>" + args.message).encode("UTF-8")
    # пауза между отправками сообщений
    t = args.time
    # количество отправок
    n = args.number
    # на какой порт посылаем
    port = args.port

    # список адресов для рассылки сообщений
    addr_list = []

    # если есть аргумент диапазона - заполняем список
    if args.range:
        # TODO check what came from that argument
        start_ip, end_ip = args.range.split("-")
        addr_list.extend(ip_range(start_ip, end_ip))

    # считаем файл с ip-шниками. Если пустая строка - то посылать будем на localhost
    if args.file:
        # файл с адресами идет в приоритете, соответственно даже если в диапазоне что-то было,
        # заполняем из файла
        addr_list = []
        # TODO try except
        with open(args.file, "r") as f:
            # отрезаем символы новой строки и запихиваем в наш список)
            # TODO check if format of ip addresses is correct
            addr_list.extend(map(str.strip, f.readlines()))
    else:
        addr_list.append("localhost")

    # создаем сокет
    server = create_server()

    # кидаем в пространство наше сообщение с интервалом time
    idx = 0
    while idx <= n:
        # пробегаемся по списку адресов и каждому посылаем сообщение
        for addr in addr_list:
            server.sendto(msg, (addr, port))

        time.sleep(t)
        idx += 1
