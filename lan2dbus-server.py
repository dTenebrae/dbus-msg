#!/usr/bin/env python

import re
import time
import socket
import argparse
import ipaddress


def ip_range(start, end) -> list:
    """
    Генерирует список ip адресов в диапазоне start-end
    start, end (string в формате "x.x.x.x")
    """
    return [
        ipaddress.ip_address(i).exploded
        for i in range(int(ipaddress.ip_address(start)),
                       int(ipaddress.ip_address(end)))
    ]


def is_ipvalid(ip_addr: str) -> bool:
    """
    source - https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp

    Проверяем валидность адреса
    """
    result = re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$", ip_addr)
    return True if result is not None else False


def get_addr(addr_range, file_name) -> list:
    """
    Функция для создания списка ip адресов
    :param addr_range: Выход с аргумента, ответственного за диапазон. str
    :param file_name: Выход с аргумента, ответственного за имя файла. str
    :return: Список адресов, если удалось что-то получить из аргументов,
    либо с localhost'ом, если там пусто
    """
    # Если пришли пустые строки
    if not addr_range and not file_name:
        return ["localhost"]

    # список адресов для рассылки сообщений
    result = []

    # если есть аргумент диапазона - заполняем список
    if addr_range:
        start_end = addr_range.split("-")
        # если длина списка не равна двум или в каком то из элементов не ip адрес - поднимаем ошибку
        if len(start_end) == 2 and (is_ipvalid(start_end[0]) & is_ipvalid(start_end[1])):
            result.extend(ip_range(start_end[0], start_end[1]))
        else:
            raise Exception("Incorrect range passed")

    # считаем файл с ip-шниками.
    if file_name:
        # файл с адресами идет в приоритете, соответственно даже если в диапазоне что-то было,
        # заполняем из файла
        result = []
        try:
            with open(file_name, "r") as f:
                # отрезаем символы новой строки и запихиваем в наш список)
                # Каждый элемент списка проверяем на соответствие шаблону ip адреса
                result.extend(filter(is_ipvalid, map(str.strip, f.readlines())))
        except FileNotFoundError:
            print("File not found")
            exit(1)

    # если наш список в итоге пустой, то рассылаем по localhost'y
    if not result:
        result.append("localhost")

    return result


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
        default=37020,
        help="Port to use. Default is 37020"
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
    # создаем сокет (семейство адресов AF_INET, протокол UDP,
    # так как нам не так уж важно дошло сообщение или нет)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.2)
    return sock


if __name__ == "__main__":
    args = parse_args()
    # сообщение для отправки. Вставляем делиметр для последующего разбора на запчасти на стороне клиента
    msg = (args.header + "<DEL>" + args.message).encode("UTF-8")
    # пауза между отправками сообщений
    t = args.time
    # количество отправок
    n = args.number
    # на какой порт посылаем
    port = args.port
    # создадим список адресов для рассылки
    addr_list = get_addr(args.range, args.file)
    # создаем сокет
    server = create_server()

    # кидаем в пространство наше сообщение с интервалом time
    idx = 0
    while idx <= n:
        # пробегаемся по списку адресов и каждому посылаем сообщение
        # TODO verbose
        for addr in addr_list:
            server.sendto(msg, (addr, port))

        time.sleep(t)
        idx += 1
