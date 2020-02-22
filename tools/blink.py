#!/usr/bin/env python3

import amonome
import time

g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1")
g.reset()
g.intensity(15)

s1 = amonome.Screen(16, 8)
s1.clear()
s2 = amonome.Screen(16, 8)
s2.set_all()

while 1:
    g.blit(s1)
    time.sleep(0.5)
    g.blit(s2)
    time.sleep(0.5)

g.close()
