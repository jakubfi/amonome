#!/usr/bin/env python3

import sys
import amonome

matrix = [[0 for x in range(8)] for x in range(16)]

# ------------------------------------------------------------------------
def process_event(e):
    if e.event == amonome.GRID_EV_BDOWN:
        if matrix[e.x][e.y] == 1:
            g.led(0, e.x, e.y)
            matrix[e.x][e.y] = 0
        else:
            g.led(1, e.x, e.y)
            matrix[e.x][e.y] = 1

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------

g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0.05)
g.reset()

while True:
    try:
        for e in g.read():
            process_event(e)
    except KeyboardInterrupt:
        print("Bye.")
        sys.exit(0)
    except Exception as e:
        print("Error communicating with amonome: %s" % str(e))

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
