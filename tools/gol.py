#!/usr/bin/python

import sys
import time
import random
import amonome

paused = False
intensity = 15
matrix = [[0 for y in xrange(8)] for x in xrange(15)]

# ------------------------------------------------------------------------
def command(y):
    global matrix
    global g
    global intensity
    global paused

    if y == 0:
        print "Intensity+"
        if intensity < 15: intensity += 1
        g.intensity(intensity)
    elif y == 1:
        print "Intensity-"
        if intensity > 1: intensity -= 1
        g.intensity(intensity)
    elif y == 2:
        paused = not paused
        print "Paused: " + str(paused)
        if paused: g.led(1, 15, 2)
        else: g.led(0, 15, 2)
    elif y == 3:
        print "Lightweight spaceship"
        matrix[0][2] = 1
        matrix[0][4] = 1
        matrix[1][5] = 1
        matrix[2][5] = 1
        matrix[3][5] = 1
        matrix[4][5] = 1
        matrix[4][4] = 1
        matrix[4][3] = 1
        matrix[3][2] = 1
    elif y == 4:
        print "Glider"
        matrix[1][0] = 1
        matrix[2][1] = 1
        matrix[0][2] = 1
        matrix[1][2] = 1
        matrix[2][2] = 1
    elif y == 5:
        print "Random block"
        px = random.randint(0, 13)
        py = random.randint(0, 6)
        matrix[px][py] = 1
        matrix[px+1][py] = 1
        matrix[px][py+1] = 1
        matrix[px+1][py+1] = 1
    elif y == 6:
        print "Random blinker"
        px = random.randint(1, 13)
        py = random.randint(1, 6)
        matrix[px][py] = 1
        matrix[px+1][py] = 1
        matrix[px-1][py] = 1
    elif y == 7:
        print "Clear"
        matrix = [[0 for y in xrange(8)] for x in xrange(15)]

    update_screen(g)

# ------------------------------------------------------------------------
def process_event(e, matrix):
    if e.event == amonome.GRID_EV_BDOWN:
        if e.x == 15:
            command(e.y)
        else:
            if matrix[e.x][e.y] == 0:
                matrix[e.x][e.y] = 1
                g.led(1, e.x, e.y)
            else:
                matrix[e.x][e.y] = 0
                g.led(0, e.x, e.y)

# ------------------------------------------------------------------------
def neighbours(m, x, y):
    n = 0
    if x > 0:
        n += m[x-1][y]
        if y > 0: n += m[x-1][y-1]
        if y < 7: n += m[x-1][y+1]

    if x < 14:
        n += m[x+1][y]
        if y > 0: n += m[x+1][y-1]
        if y < 7: n += m[x+1][y+1]

    if y > 0: n += m[x][y-1]
    if y < 7: n += m[x][y+1]
    return n

# ------------------------------------------------------------------------
def update_game(m):
    new_matrix = [[0 for y in xrange(8)] for x in xrange(15)]

    for x in xrange(15):
        for y in xrange(8):
            if m[x][y]:
                if neighbours(m, x, y) < 2:
                    new_matrix[x][y] = 0
                elif neighbours(m, x, y) <= 3:
                    new_matrix[x][y] = 1
                elif neighbours(m, x, y) > 3:
                    new_matrix[x][y] = 0
            else:
                if neighbours(m, x, y) == 3:
                    new_matrix[x][y] = 1

    return new_matrix

# ------------------------------------------------------------------------
def update_screen(g):
    for x in xrange(15):
        data = 0
        for y in xrange(8):
            data += 2**y * matrix[x][7-y]
        g.led_column(x, data)
    pass

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------

random.seed()

try:
    g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0.05)
    g.reset()
except Exception, e:
    print "Cannot initialize amonome: %s" % str(e)
    sys.exit(1)

while True:
    time_spent = 0
    start_tick = time.time()
    while time_spent < 1/5.0:
        try:
            for e in g.read():
                process_event(e, matrix)
        except KeyboardInterrupt:
            print "Bye."
            sys.exit(0)
        time_spent = time.time() - start_tick

    if not paused: matrix = update_game(matrix)
    update_screen(g)

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
