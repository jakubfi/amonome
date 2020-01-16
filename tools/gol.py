#!/usr/bin/env python3

import sys
import time
import random
import amonome

paused = False
intensity = 15
matrix = [[0 for y in range(8)] for x in range(15)]

frame_time = 1/8.0

# ------------------------------------------------------------------------
def command(y):
    global matrix
    global g
    global intensity
    global paused
    global frame_time

    frame_delta = 1.0/128.0

    if y == 0:
        print("Speed+")
        if frame_time > frame_delta:
            frame_time -= frame_delta
    elif y == 1:
        print("Speed-")
        if frame_time < 1.0/4.0:
            frame_time += frame_delta
    elif y == 2:
        paused = not paused
        print("Paused: %s" % str(paused))
        if paused: g.led(1, 15, 2)
        else: g.led(0, 15, 2)
    elif y == 3:
        print("Lightweight spaceship")
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
        print("Glider")
        matrix[1][0] = 1
        matrix[2][1] = 1
        matrix[0][2] = 1
        matrix[1][2] = 1
        matrix[2][2] = 1
    elif y == 5:
        print("Random block")
        px = random.randint(0, 13)
        py = random.randint(0, 6)
        matrix[px][py] = 1
        matrix[px+1][py] = 1
        matrix[px][py+1] = 1
        matrix[px+1][py+1] = 1
    elif y == 6:
        print("Random blinker")
        px = random.randint(1, 13)
        py = random.randint(1, 6)
        matrix[px][py] = 1
        matrix[px+1][py] = 1
        matrix[px-1][py] = 1
    elif y == 7:
        print("Clear")
        matrix = [[0 for y in range(8)] for x in range(15)]

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
        elif y == 0: n += m[x-1][7]
        if y < 7: n += m[x-1][y+1]
        elif y == 7: n += m[x-1][0]
    elif x == 0:
        n += m[14][y]
        if y > 0: n += m[14][y-1]
        elif y == 0: n += m[14][7]
        if y < 7: n += m[14][y+1]
        elif y == 7: n += m[14][0]

    if x < 14:
        n += m[x+1][y]
        if y > 0: n += m[x+1][y-1]
        elif y == 0: n += m[x+1][7]
        if y < 7: n += m[x+1][y+1]
        elif y == 7: n += m[x+1][0]
    elif x == 14:
        n += m[0][y]
        if y > 0: n += m[0][y-1]
        elif y == 0: n += m[0][7]
        if y < 7: n += m[0][y+1]
        elif y == 7: n += m[0][0]

    if y > 0: n += m[x][y-1]
    elif y == 0: n += m[x][7]
    if y < 7: n += m[x][y+1]
    elif y == 7: n += m[x][0]

    return n

# ------------------------------------------------------------------------
def update_game(m):
    new_matrix = [[0 for y in range(8)] for x in range(15)]

    for x in range(15):
        for y in range(8):
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
    for x in range(15):
        data = 0
        for y in range(8):
            data += 2**y * matrix[x][7-y]
        g.led_column(x, data)
    pass

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------

random.seed()

g = amonome.Amonome("/dev/ttyUSB0", "/dev/ttyUSB1", 0.05)
g.reset()

while True:
    time_spent = 0
    start_tick = time.time()
    while time_spent < frame_time:
        try:
            for e in g.read():
                process_event(e, matrix)
        except KeyboardInterrupt:
            print("Bye.")
            sys.exit(0)
        time_spent = time.time() - start_tick

    if not paused: matrix = update_game(matrix)
    update_screen(g)

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
