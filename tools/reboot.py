#!/usr/bin/python

import sys

from amonome import Grid8x8

g1 = Grid8x8("/dev/ttyUSB0", 0)
g2 = Grid8x8("/dev/ttyUSB1", 0)

if len(sys.argv) == 2:
    if sys.argv[1] == "a":
        g1.reboot()
    elif sys.argv[1] == "b":
        g2.reboot()
else:
    g1.reboot()
    g2.reboot()

g1.close()
g2.close()
