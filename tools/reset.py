#!/usr/bin/env python2

from amonome import Amonome

g = Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)

g.reset()

g.close();
