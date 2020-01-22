#!/usr/bin/env python3

import sys
import time
import random
import amonome

numbers = [
[
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 0,0,0,0 ],
],
[
[ 0,0,1,0 ],
[ 0,1,1,0 ],
[ 0,0,1,0 ],
[ 0,0,1,0 ],
[ 0,0,1,0 ],
[ 0,0,1,0 ],
[ 0,1,1,1 ],
[ 0,0,0,0 ],
],
[
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 0,0,0,1 ],
[ 0,0,1,0 ],
[ 0,1,0,0 ],
[ 1,0,0,0 ],
[ 1,1,1,1 ],
[ 0,0,0,0 ],
],
[
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 0,0,0,1 ],
[ 0,0,1,0 ],
[ 0,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 0,0,0,0 ],
],
[
[ 1,0,0,0 ],
[ 1,0,0,0 ],
[ 1,0,1,0 ],
[ 1,1,1,1 ],
[ 0,0,1,0 ],
[ 0,0,1,0 ],
[ 0,0,1,0 ],
[ 0,0,0,0 ],
],
[
[ 1,1,1,1 ],
[ 1,0,0,0 ],
[ 1,0,0,0 ],
[ 1,1,1,0 ],
[ 0,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 0,0,0,0 ],
],
[
[ 0,0,1,0 ],
[ 0,1,0,0 ],
[ 1,0,0,0 ],
[ 1,1,1,0 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 0,0,0,0 ],
],
[
[ 1,1,1,1 ],
[ 0,0,0,1 ],
[ 0,0,1,0 ],
[ 0,1,0,0 ],
[ 0,1,0,0 ],
[ 0,1,0,0 ],
[ 0,1,0,0 ],
[ 0,0,0,0 ],
],
[
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,0 ],
[ 0,0,0,0 ],
],
[
[ 0,1,1,0 ],
[ 1,0,0,1 ],
[ 1,0,0,1 ],
[ 0,1,1,1 ],
[ 0,0,0,1 ],
[ 0,0,1,0 ],
[ 0,1,0,0 ],
[ 0,0,0,0 ],
],
]

sad = [
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0 ],
[ 0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
]

empty = [
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
]

go = [
[
[ 0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0 ],
],
[
[ 0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0 ],
],
[
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0 ],
],
[
[ 0,0,1,1,1,0,0,0,0,1,1,0,0,0,1,1 ],
[ 0,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1 ],
[ 1,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1 ],
[ 1,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1 ],
[ 1,1,0,1,1,1,0,1,1,0,0,1,1,0,1,1 ],
[ 1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,0 ],
[ 0,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1 ],
[ 0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,1 ],
]
]

intro = [
[
[ 0,0,0,1,1,0,1,1,1,0,1,1,1,0,0,0 ],
[ 0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0 ],
[ 0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0 ],
[ 0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0 ],
[ 0,0,1,1,0,0,1,1,1,0,0,1,0,0,0,0 ],
],
[
[ 0,1,1,0,0,0,1,0,0,1,0,1,0,1,1,1 ],
[ 1,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0 ],
[ 1,0,1,1,0,1,1,1,0,1,0,1,0,1,1,1 ],
[ 1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0 ],
[ 0,1,1,0,0,1,0,1,0,1,0,1,0,1,1,1 ],
],
[
[ 1,0,0,1,1,0,1,0,1,0,1,1,0,1,0,0 ],
[ 1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0 ],
[ 1,0,0,1,1,0,1,0,1,0,1,1,0,1,0,0 ],
[ 1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0 ],
[ 1,1,0,1,1,0,0,1,0,0,1,1,0,1,1,0 ],
],
]

# ------------------------------------------------------------------------
class Point:
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # --------------------------------------------------------------------
    def __str__(self):
        return "(%i, %i)" % (self.x, self.y)

    # --------------------------------------------------------------------
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # --------------------------------------------------------------------
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

# ------------------------------------------------------------------------
class Game:
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, port_a, port_b, hz=60):
        self.hz = hz
        self.frame_time = 1.0 / self.hz
        self.s = amonome.Amonome(port_a, port_b, self.frame_time)
        self.s.reset()
        print("Surface on %s and %s initialized for %i Hz (frame time: %.2f)" % (port_a, port_b, hz, self.frame_time))

    # --------------------------------------------------------------------
    def event_process(self, e):
        print(e)

    # --------------------------------------------------------------------
    def logic_tick(self):
        print("=== TICK %d Hz ===" % self.hz)

    # --------------------------------------------------------------------
    def game_over(self):
        print("GAME OVER")

    # --------------------------------------------------------------------
    def run(self):
        while True:
            t_spent = 0
            t_start = time.time()
            while t_spent < self.frame_time:
                for e in self.s.read():
                    self.event_process(e)
                t_spent = time.time() - t_start

            if self.logic_tick() == False:
                self.game_over()
                break

# ------------------------------------------------------------------------
class Level(Game):
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, port_a, port_b, hz=60):
        Game.__init__(self, port_a, port_b, hz)
        self.screen = amonome.Screen(16, 8)
        self.level = 0
        self.ticks = 0
        self.page = -1
        self.flip_page()

    # --------------------------------------------------------------------
    def event_process(self, ev):
        if ev.event == amonome.GRID_EV_BDOWN and (ev.y == 6 or ev.y == 7):
            if ev.x == 4:
                self.level = 3
            elif ev.x == 6:
                self.level = 5
            elif ev.x == 8:
                self.level = 7
            elif ev.x == 10:
                self.level = 10
            elif ev.x == 12:
                self.level = 15

    # --------------------------------------------------------------------
    def flip_page(self):
        self.page += 1
        if self.page >= len(intro):
            self.page = 0
        for i in range(3):
            self.screen.import_array(0, 0, empty)
            self.s.blit(self.screen)
            self.s.led(True, 4, 6)
            self.s.led(True, 6, 6)
            self.s.led(True, 8, 6)
            self.s.led(True, 10, 6)
            self.s.led(True, 12, 6)
            time.sleep(0.01)
            self.screen.import_array(0, 0, intro[self.page])
            self.s.blit(self.screen)
            self.s.led(True, 4, 6)
            self.s.led(True, 6, 6)
            self.s.led(True, 8, 6)
            self.s.led(True, 10, 6)
            self.s.led(True, 12, 6)
            time.sleep(0.05)

    # --------------------------------------------------------------------
    def get_ready(self):
        for i in range(3,4):
            for x in range(16):
                self.screen.line_vert(x, 0, 8)
                self.s.blit(self.screen)
                time.sleep(0.01)
            for xb in range(16):
                self.screen.import_array(0, 0, go[i])
                for x in range(xb, 16):
                    self.screen.line_vert(x, 0, 8)
                self.s.blit(self.screen)
                time.sleep(0.01)
            self.screen.import_array(0, 0, go[i])
            self.s.blit(self.screen)
            time.sleep(0.6)

    # --------------------------------------------------------------------
    def logic_tick(self):
        if not self.level:
            if self.ticks < 4:
                self.ticks += 1
            else:
                self.ticks = 0
                self.flip_page()
        else:
            self.get_ready()
            return False


# ------------------------------------------------------------------------
class Glizda(Game):
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, port_a, port_b, hz=60):
        Game.__init__(self, port_a, port_b, hz)
        self.screen = amonome.Screen(16, 8)
        random.seed()
        self.reset()

    # --------------------------------------------------------------------
    def reset(self):
        self.v = Point(1, 0)
        self.new_v = self.v
        self.glizda = [Point(1, 2), Point(2, 2), Point(3, 2)]
        self.max_len = len(self.glizda)
        self.add_food()

    # --------------------------------------------------------------------
    def event_process(self, ev):
        if ev.event == amonome.GRID_EV_BDOWN:
            if self.v.x != 0:
                if ev.y > self.glizda[-1].y:
                    self.set_vector(Point(0, 1)) # Down
                elif ev.y < self.glizda[-1].y:
                    self.set_vector(Point(0, -1)) # Up
            else:
                if ev.x > self.glizda[-1].x:
                    self.set_vector(Point(1, 0)) # Right
                elif ev.x < self.glizda[-1].x:
                    self.set_vector(Point(-1, 0)) # Left

    # --------------------------------------------------------------------
    def set_vector(self, direction):
        self.new_v = direction

    # --------------------------------------------------------------------
    def game_over(self):
        print("Score: %i" % self.max_len)
        for i in range(10):
            self.s.intensity(2)
            time.sleep(0.05)
            self.s.intensity(15)
            time.sleep(0.05)
        n1 = int(self.max_len/10)
        n2 = int(self.max_len%10)
        if self.max_len < 10:
            self.screen.import_array(6, 0, numbers[n2])
        else:
            self.screen.import_array(3, 0, numbers[n1])
            self.screen.import_array(9, 0, numbers[n2])
        self.s.blit(self.screen)
        time.sleep(2)
        self.s.reset()

    # --------------------------------------------------------------------
    def add_food(self):
        x = random.randint(0, 15)
        y = random.randint(0, 7)
        self.food = Point(x, y)
        while self.food in self.glizda:
            x = random.randint(0, 15)
            y = random.randint(0, 7)
            self.food = Point(x, y)
        self.s.led(True, self.food.x, self.food.y)
        print(self.food)

    # --------------------------------------------------------------------
    def logic_tick(self):
        # activate new vector
        if self.new_v:
            self.v = self.new_v

        # calculate new head
        head = self.glizda[-1]
        nhead = head + self.v

        # check for walls/self collisions
        if nhead.x > 15 or nhead.x < 0 or nhead.y > 7 or nhead.y < 0 or nhead in self.glizda:
            return False

        # grow the worm
        self.glizda.append(nhead)
        self.s.led(True, nhead.x, nhead.y)

        # check for food collision
        if self.food == nhead:
            self.s.led(False, nhead.x, nhead.y)
            time.sleep(0.02)
            self.s.led(True, nhead.x, nhead.y)
            time.sleep(0.02)
            self.s.led(False, nhead.x, nhead.y)
            time.sleep(0.02)
            self.s.led(True, nhead.x, nhead.y)
            time.sleep(0.02)
            self.max_len += 1
            self.add_food()

        # move the worm
        while len(self.glizda) > self.max_len:
            self.s.led(False, self.glizda[0].x, self.glizda[0].y)
            del self.glizda[0]


# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------

while True:
    level = Level("/dev/ttyUSB0", "/dev/ttyUSB1", 5)
    level.run()

    game = Glizda("/dev/ttyUSB0", "/dev/ttyUSB1", level.level)
    game.run()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
