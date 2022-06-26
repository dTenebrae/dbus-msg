# lan2dbus

**Описание**

Небольшое приложение, занимающееся рассылкой от сервера к клиентам сообщения, которое появляется системным уведомлением (через dbus notification)

#### Структура проекта

```
├── README.md
├── build
│   └── aarch64
│       ├── lan2dbus-client-0.1-1.el7.aarch64.rpm
│       └── lan2dbus-server-0.1-1.el7.aarch64.rpm
├── requirements.txt
├── spec
│   ├── lan2dbus-client.spec
│   └── lan2dbus-server.spec
└── src
    ├── l2dbclient.service
    ├── l2dbclient.timer
    ├── lan2dbus-client.py
    └── lan2dbus-server.py
```


#### Сборка RPM-пакета


```
# Устанавливаем необходимые инструменты
$ sudo dnf install rpm-build rpm-devel rpmdevtools
$ pip3 install --user pyinstaller

# Создаем сборочные директории
$ rpmdev-setuptree

# копируем сорцы
$ cp src/* $HOME/rpmbuild/SOURCES/

# копируем спеки
$ cp spec/* $HOME/rpmbuild/SPECS/

# собираем клиент
$ rpmbuild -ba $HOME/rpmbuild/SPECS/lan2dbus-client.spec

# собираем сервер
$ rpmbuild -ba $HOME/rpmbuild/SPECS/lan2dbus-server.spec
```

#### Установка в систему

__Client__

```
$ sudo dnf install -y lan2dbus-client-0.1-1.el7.aarch64.rpm

# Если требуется, стартуем службу. Она будет опрашивать порт каждые 10 секунд
$ sudo systemctl start l2dbclient.timer

# Разрешаем выводить на DISPLAY
$ xhost +
```

__Server__

```
sudo dnf install -y lan2dbus-server-0.1-1.el7.aarch64.rpm
```

#### Использование

__lan2dbus-server__

```
usage: lan2dbus-server [-h] [-m MESSAGE] [-H HEADER] [-t TIME] [-n NUMBER] [-p PORT] [-f FILE] [-r RANGE]

Server side of message broadcasting app

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        Message to send over LAN
  -H HEADER, --header HEADER
                        Header of popup window on client side
  -t TIME, --time TIME  Time(sec) to sleep between sending another message. Default is 1
  -n NUMBER, --number NUMBER
                        Number of messages you want to send. Default is 9999
  -p PORT, --port PORT  Port to use. Default is 37020
  -f FILE, --file FILE  Path to file with ip addresses. Default is empty string, which leads to localhost
  -r RANGE, --range RANGE
                        Range of ip addresses. Example: 192.168.1.1-192.168.1.255. Default is none
```

__lan2dbus-client__

```
usage: lan2dbus-client [-h] [-p PORT]

Client side of message broadcasting app

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen. Default is 37020
```

#### Удаление

```
# останавливаем клиентскую службу (если была запущена)
$ sudo systemctl stop l2dbclient.timer
$ sudo systemctl daemon-reload
$ sudo systemctl reset-failed

# удаляем пакет из системы
$ sudo dnf remove -y lan2dbus-client-0.1-1.el7.aarch64.rpm
$ sudo dnf remove -y lan2dbus-server-0.1-1.el7.aarch64.rpm
```

#### Dependencies

Для запуска вручную, либо если в процессе установки не загрузились зависимости

* pip3 install dbus-python
* sudo dnf install -y python3-devel dbus-devel glib2-devel
