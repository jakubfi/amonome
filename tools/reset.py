#!/usr/bin/python

from amonome import Amonome

g = Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)

g.reset()

g.close();
