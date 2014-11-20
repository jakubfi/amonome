#!/usr/bin/python

from amonome import Amonome

g = Amonome("/dev/ttyUSB0", "/dev/ttyUSB1")

g.reset()

while 1:
    g.read()
