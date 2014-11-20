#!/usr/bin/python

import sys

from amonome import Grid

g1 = Grid("/dev/ttyUSB0")
g2 = Grid("/dev/ttyUSB1")

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
