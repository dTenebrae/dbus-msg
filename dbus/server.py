#!/usr/bin/env python

#Python DBUS Test Server
#runs until the Quit() method is called via DBUS

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import argparse

class MyDBUSService(dbus.service.Object):
    def __init__(self, msg: str):
        self.text = msg
        bus_name = dbus.service.BusName('org.my.test', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/my/test')

    @dbus.service.method('org.my.test')
    def hello(self):
        return self.text

    # @dbus.service.method('org.my.test')
    # def string_echo(self, s):
        # """returns whatever is passed to it"""
        # return s

    @dbus.service.method('org.my.test')
    def Quit(self):
        """removes this object from the DBUS connection and exits"""
        self.remove_from_connection()
        Gtk.main_quit()
        return

def parse_args():
    parser = argparse.ArgumentParser(description="Simple dbus message server")
    parser.add_argument(
        '-t',
        '--text',
        type=str,
        default="Killing time",
        help="Message you want to send"
    )
    return parser.parse_args()

if __name__ == "__main__":
    # ####### initial values ###########
    args = parse_args()
    TEXT = args.text
    # ##################################

    DBusGMainLoop(set_as_default=True)
    myservice = MyDBUSService(TEXT)
    Gtk.main()
