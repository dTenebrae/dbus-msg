# lan2dbus

**Описание**

Небольшое приложение, занимающееся рассылкой от сервера к клиентам сообщения, которое появляется системным уведомлением (через dbus notification)

* la2dbus-server 

```
usage: lan2dbus-server.py [-h] [-m MESSAGE] [-H HEADER] [-t TIME] [-n NUMBER] [-p PORT] [-f FILE] [-r RANGE]

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
  -p PORT, --port PORT  Port to use. Default is 9999
  -f FILE, --file FILE  Path to file with ip addresses. Default is empty string, which leads to localhost
  -r RANGE, --range RANGE
                        Range of ip addresses. Example: 192.168.1.1-192.168.1.255. Default is none
```


### Зависимости

* dbus-python (need to install: sudo dnf install -y python3-devel dbus-devel glib2-devel)


_work in progress_