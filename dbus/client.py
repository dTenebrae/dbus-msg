#!/usr/bin/env python

#Python script to call the methods of the DBUS Test Server

import dbus
import subprocess

def show_msg(msg):
    subprocess.Popen(['notify-send', msg])
    return

#get the session bus
bus = dbus.SessionBus()
#get the object
the_object = bus.get_object("org.my.test", "/org/my/test")
#get the interface
the_interface = dbus.Interface(the_object, "org.my.test")

#call the methods and print the results
reply = the_interface.hello()
show_msg(reply)

# reply = the_interface.string_echo("test 123")
# print(reply)

# the_interface.Quit()
