#!/usr/bin/env python3

import amonome
import time

g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)
g.reset()
g.intensity(15)

s1 = amonome.Screen(16, 8)
s1.clear()
s2 = amonome.Screen(16, 8)
s2.set()

while 1:
    g.blit(s1)
    time.sleep(0.04)
    g.blit(s2)
    time.sleep(0.04)

g.close()
