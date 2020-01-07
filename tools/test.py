#!/usr/bin/env python2

import time
from amonome import *

g = Grid8x8("/dev/ttyUSB0", 0)

g.led(1,1,1)
time.sleep(0.5)
g.led(0,1,1)
time.sleep(0.5)

g.close()
