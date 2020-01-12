#!/usr/bin/env python3

from amonome import Amonome

g = Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)

g.reset()

g.close();
