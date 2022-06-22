#!/usr/bin/env python

#Python script to call the methods of the DBUS Test Server

import dbus

#get the session bus
bus = dbus.SessionBus()
#get the object
the_object = bus.get_object("org.my.test", "/org/my/test")
#get the interface
the_interface = dbus.Interface(the_object, "org.my.test")

#call the methods and print the results
reply = the_interface.hello()
print(reply)

# reply = the_interface.string_echo("test 123")
# print(reply)

# the_interface.Quit()
