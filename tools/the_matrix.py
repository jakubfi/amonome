#!/usr/bin/env python3

import sys
import amonome
import random
import time

STATE_DEAD = 0
STATE_LIVE = 1

drop_count = 6 * 8
SPEED_MIN = 50
SPEED_MAX = 250
LEN_MIN = 2
LEN_MAX = 8
POS_MAX = 60

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
            self.len = random.randint(LEN_MIN, LEN_MAX)
            self.speed = random.randint(SPEED_MIN, SPEED_MAX)
            self.pos = -self.len
            self.state = STATE_LIVE
            print("%i : speed %.4f, len %i" % (self.num, self.speed, self.len))
        elif self.state == STATE_LIVE:
            self.pos += self.speed / 1000.0
            if self.pos > POS_MAX:
                self.state = STATE_DEAD

    # --------------------------------------------------------------------
    def display(self):
        start = int(self.pos) if self.pos >= 0 else 0
        end = int(self.pos+self.len) if self.pos+self.len <= 16 else 16
        s.line_horiz(start, self.num % 8, end-start)

drop = []

# ------------------------------------------------------------------------
def update(t, s):
    s.clear()
    for i in range(drop_count):
        drop[i].advance(t)
        drop[i].display()

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------
g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0)
g.reset()

s = amonome.Screen(16, 8)

for i in range(drop_count):
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
    print("Bye.")

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
