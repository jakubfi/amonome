#!/usr/bin/env python2

import sys
import amonome
import random
import time

STATE_DEAD = 0
STATE_HOLD = 1
STATE_LIVE = 2

# ------------------------------------------------------------------------
class Drop:
    # --------------------------------------------------------------------
    def __init__(self, s, num):
        self.s = s
        self.state = STATE_DEAD
        self.live = 0
        self.speed = 0
        self.len = 0
        self.pos = 0
        self.num = num

    # --------------------------------------------------------------------
    def advance(self, t):
        if self.state == STATE_DEAD:
            self.speed = random.randint(60, 300) / 1000.0
            self.len = random.randint(1, 7)
            self.range = random.randint(16, 50)
            self.pos = -self.len
            self.state = STATE_LIVE
            print("%i : speed %.4f, len %i, range %i" % (self.num, self.speed, self.len, self.range))
        elif self.state == STATE_LIVE:
            self.pos += self.speed
            if self.pos > self.range:
                self.state = STATE_DEAD

    # --------------------------------------------------------------------
    def display(self):
        start = int(self.pos) if self.pos >= 0 else 0
        end = int(self.pos+self.len) if self.pos+self.len <= 16 else 16
        s.line_horiz(start, self.num, end-start)

drop = []

# ------------------------------------------------------------------------
def update(t, s):
    s.clear()
    for i in range(8):
        drop[i].advance(t)
        drop[i].display()

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------
try:
    g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)
    g.reset()
except Exception, e:
    print "Cannot initialize amonome: %s" % str(e)
    sys.exit(1)

s = amonome.Screen(16, 8)

for i in range(8):
    drop.append(Drop(s, i))

delta = 0.01
tsec = 0
try:
    while True:
        update(tsec, s)
        g.blit(s)
        time.sleep(delta)
        tsec += delta

except KeyboardInterrupt:
    print "Bye."

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
