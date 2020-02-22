#!/usr/bin/env python3

import sys
import time
import random
import amonome
from point import Point
from game import Game

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
class GlizdaLevel(Game):
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, width, height, port_a, port_b, hz=60):
        Game.__init__(self, width, height, port_a, port_b, hz)
        self.level = 0
        self.movable_food = True
        self.absolute_control = False
        self.ticks = 0
        self.page = 0

    # --------------------------------------------------------------------
    def event_process(self, ev):
        if ev.event == amonome.GRID_EV_BDOWN:
            if ev.x == 0 and ev.y == 0:
                self.movable_food = False
            if ev.x == 15 and ev.y == 0:
                self.absolute_control = True
            if ev.y == 6 or ev.y == 7:
                if ev.x == 4:
                    self.level = 1
                elif ev.x == 6:
                    self.level = 5
                elif ev.x == 8:
                    self.level = 7
                elif ev.x == 10:
                    self.level = 10
                elif ev.x == 12:
                    self.level = 15

    # --------------------------------------------------------------------
    def game_over(self):
        print("Selected level: {} (food is {})".format(self.level, "movable" if self.movable_food else "static"))

    # --------------------------------------------------------------------
    def draw(self):
        self.screen.import_array(0, 0, intro[self.page])
        self.screen.set(True, 4, 6)
        self.screen.set(True, 6, 6)
        self.screen.set(True, 8, 6)
        self.screen.set(True, 10, 6)
        self.screen.set(True, 12, 6)

    # --------------------------------------------------------------------
    def flip_page(self):
        self.page += 1
        if self.page >= len(intro):
            self.page = 0
        for i in range(3):
            self.screen.import_array(0, 0, empty)
            self.screen.set(True, 4, 6)
            self.screen.set(True, 6, 6)
            self.screen.set(True, 8, 6)
            self.screen.set(True, 10, 6)
            self.screen.set(True, 12, 6)
            self.s.blit(self.screen)
            time.sleep(0.01)
            self.screen.import_array(0, 0, intro[self.page])
            self.screen.set(True, 4, 6)
            self.screen.set(True, 6, 6)
            self.screen.set(True, 8, 6)
            self.screen.set(True, 10, 6)
            self.screen.set(True, 12, 6)
            self.s.blit(self.screen)
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
class Glizda:
# ------------------------------------------------------------------------
    DIR_UP = 1
    DIR_DOWN = 2
    DIR_LEFT = 3
    DIR_RIGHT = 4

    def __init__(self):
        self.food = 0
        self.reset()

    def reset(self):
        self.vector = Point(0, 0)

        self.body = [Point(1, 2), Point(2, 2), Point(3, 2)]
        self.set_direction(Glizda.DIR_RIGHT)

        #self.body = [
        #    Point(0,0),Point(1,0),Point(2,0),Point(3,0),Point(4,0),Point(5,0),Point(6,0),Point(7,0),Point(8,0),Point(9,0),Point(10,0),Point(11,0),Point(12,0),Point(13,0),Point(14,0),Point(15,0),
        #    Point(15,1),Point(14,1),Point(13,1),Point(12,1),Point(11,1),Point(10,1),Point(9,1),Point(8,1),Point(7,1),Point(6,1),Point(5,1),Point(4,1),Point(3,1),Point(2,1),Point(1,1),Point(0,1),
        #    Point(0,2),Point(1,2),Point(2,2),Point(3,2),Point(4,2),Point(5,2),Point(6,2),Point(7,2),Point(8,2),Point(9,2),Point(10,2),Point(11,2),Point(12,2),Point(13,2),Point(14,2),Point(15,2),
        #    Point(15,3),Point(14,3),Point(13,3),Point(12,3),Point(11,3),Point(10,3),Point(9,3),Point(8,3),Point(7,3),Point(6,3),Point(5,3),Point(4,3),Point(3,3),Point(2,3),Point(1,3),Point(0,3),
        #    Point(0,4),Point(1,4),Point(2,4),Point(3,4),Point(4,4),Point(5,4),Point(6,4),Point(7,4),Point(8,4),Point(9,4),Point(10,4),Point(11,4),Point(12,4),Point(13,4),Point(14,4),Point(15,4),
        #    Point(15,5),Point(14,5),Point(13,5),Point(12,5),Point(11,5),Point(10,5),Point(9,5),Point(8,5),Point(7,5),Point(6,5),Point(5,5),Point(4,5),Point(3,5),Point(2,5),Point(1,5),Point(0,5),
        #    Point(0,6),Point(1,6),Point(2,6),Point(3,6),Point(4,6),Point(5,6),Point(6,6),Point(7,6),Point(8,6),Point(9,6),Point(10,6),Point(11,6),Point(12,6),Point(13,6),Point(14,6),Point(15,6),
        #    Point(15,7)
        #]
        #self.length = len(self.body)
        #self.set_direction(Glizda.DIR_LEFT)

        self.length = len(self.body)

    def head(self):
        return self.body[-1]

    def feed(self):
        self.food += 1

    def advance(self):
        res = self.grow()
        if self.food > 0:
            self.food -= 1
        else:
            self.shrink()

        return res

    def grow(self):
        new_head = self.head() + self.vector
        if new_head in self.body:
            return False
        self.length += 1
        self.body.append(new_head)
        return True

    def shrink(self):
        self.length -= 1
        del self.body[0]

    def set_direction(self, direction):
        if direction == Glizda.DIR_UP:
            vector = Point(0, -1)
        elif direction == Glizda.DIR_DOWN:
            vector = Point(0, 1)
        elif direction == Glizda.DIR_LEFT:
            vector = Point(-1, 0)
        elif direction == Glizda.DIR_RIGHT:
            vector = Point(1, 0)
        else:
            pass

        if vector.x != self.vector.x or vector.y != self.vector.y:
            self.direction = direction
            self.vector = vector

# ------------------------------------------------------------------------
class Food:
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, probability, min_distance, grace_period):
        self.probability = probability
        self.min_distance = min_distance
        self.grace_period = grace_period
        self.pos = None

    # --------------------------------------------------------------------
    def add(self, allowed_positions):
        try:
            self.pos = random.sample(allowed_positions, 1)[0]
            if self.grace_period >= 0:
                self.grace_period -= 1
            print("Added food at {}".format(str(self.pos)))
        except:
            pass

    # --------------------------------------------------------------------
    def remove(self):
        self.pos = None

    # --------------------------------------------------------------------
    def try_moving(self, allowed_positions, predator_head):
        if self.grace_period >= 0:
            return
        if self.pos.dist(predator_head) > self.min_distance:
            return
        if random.random() >= self.probability:
            return
        allowed_moves = set([
            self.pos+Point(0, 1),
            self.pos+Point(0, -1),
            self.pos+Point(1, 0),
            self.pos+Point(-1, 0),
        ])
        dest = random.sample(allowed_moves & allowed_positions, 1)
        if dest:
            self.pos = dest[0]

       
# ------------------------------------------------------------------------
class GlizdaGame(Game):
# ------------------------------------------------------------------------
    
    # --------------------------------------------------------------------
    def __init__(self, width, height, port_a, port_b, hz, movable_food, absolute_control):
        Game.__init__(self, width, height, port_a, port_b, hz)
        self.whole_world = set([Point(x, y) for x in range(self.width) for y in range(self.height)])
        self.glizda = Glizda()
        self.absolute_control = absolute_control
        if movable_food:
            self.food = Food(probability=0.5, min_distance=3, grace_period=6)
        else:
            self.food = Food(probability=0, min_distance=0, grace_period=200)
        initial_food_zone = set([Point(x, y) for x in range(self.width//2+2, self.width) for y in range(self.height)])
        self.food.add(initial_food_zone & self.empty_fields())
        self.had_meal = False

    # --------------------------------------------------------------------
    def empty_fields(self):
        return self.whole_world - set(self.glizda.body)

    # --------------------------------------------------------------------
    def event_process(self, ev):
        new_dir = self.glizda.direction

        if ev.event == amonome.GRID_EV_BDOWN:
            if self.absolute_control:
                if ev.y == 6 and (ev.x == 14 or ev.x == 1):
                    new_dir = Glizda.DIR_UP
                elif ev.y == 7:
                    if ev.x == 13 or ev.x == 0:
                        new_dir = Glizda.DIR_LEFT
                    elif ev.x == 14 or ev.x == 1:
                        new_dir = Glizda.DIR_DOWN
                    elif ev.x == 15 or ev.x == 2:
                        new_dir = Glizda.DIR_RIGHT
            else:
                if self.glizda.direction in [Glizda.DIR_LEFT, Glizda.DIR_RIGHT]:
                    if ev.y > self.glizda.head().y:
                        new_dir = Glizda.DIR_DOWN
                    elif ev.y < self.glizda.head().y:
                        new_dir = Glizda.DIR_UP
                else:
                    if ev.x > self.glizda.head().x:
                        new_dir = Glizda.DIR_RIGHT
                    elif ev.x < self.glizda.head().x:
                        new_dir = Glizda.DIR_LEFT

            if new_dir != self.glizda.direction:
                self.glizda.set_direction(new_dir)

    # --------------------------------------------------------------------
    def game_over(self):
        print("Score: %i" % self.glizda.length)

        cycles = 10
        for i in range(cycles):
            self.s.intensity(0)
            time.sleep(0.04)
            brightness = int(15 - 15*i/cycles)
            self.s.intensity(brightness)
            time.sleep(0.04)

        l = self.glizda.length
        n0 = int(l / 100)
        n1 = int((l-100*n0) / 10)
        n2 = int(l%10)

        self.screen.clear()
        if self.glizda.length < 10:
            self.screen.import_array(6, 0, numbers[n2])
        elif self.glizda.length < 100:
            self.screen.import_array(3, 0, numbers[n1])
            self.screen.import_array(9, 0, numbers[n2])
        elif self.glizda.length < 1000:
            self.screen.import_array(0, 0, numbers[n0])
            self.screen.import_array(6, 0, numbers[n1])
            self.screen.import_array(12, 0, numbers[n2])

        self.s.blit(self.screen)
        self.s.intensity(15)
        time.sleep(1)

    # --------------------------------------------------------------------
    def draw(self):
        for i in self.glizda.body:
            if i.x >= 0 and i.x < self.width and i.y >= 0 and i.y < self.height:
                self.screen.set(True, i.x, i.y)
        if self.food.pos:
            self.screen.set(True, self.food.pos.x, self.food.pos.y)

    # --------------------------------------------------------------------
    def logic_tick(self):

        if not self.glizda.advance():
            print("Collision: self")
            return False

        hd = self.glizda.head()

        if hd.x >= self.width or hd.x < 0 or hd.y >= self.height or hd.y < 0:
            print("Collision: border")
            return False

        if hd == self.food.pos:
            self.glizda.feed()
            print("Food eaten (len: {})".format(self.glizda.length))
            self.s.led(False, hd.x, hd.y)
            time.sleep(0.02)
            self.s.led(True, hd.x, hd.y)
            time.sleep(0.02)
            self.s.led(False, hd.x, hd.y)
            time.sleep(0.02)
            self.s.led(True, hd.x, hd.y)
            time.sleep(0.02)
            self.food.remove()
            self.food.add(self.empty_fields())
        else:
            self.food.try_moving(self.empty_fields(), hd)

# ------------------------------------------------------------------------
# --- MAIN ---------------------------------------------------------------
# ------------------------------------------------------------------------

while True:
    level = GlizdaLevel(16, 8, "/dev/ttyUSB0", "/dev/ttyUSB1", 5)
    level.run()

    game = GlizdaGame(16, 8, "/dev/ttyUSB0", "/dev/ttyUSB1", level.level, level.movable_food, level.absolute_control)
    game.run()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
