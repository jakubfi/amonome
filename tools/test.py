#!/usr/bin/env python

import time
from amonome import *

g = Grid("/dev/ttyUSB0")

g.led(1,1,1)
time.sleep(0.5)
g.led(0,1,1)
time.sleep(0.5)

g.close()
