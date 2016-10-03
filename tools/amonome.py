#  Copyright (c) 2014 Jakub Filipowicz <jakubf@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import serial
import time

GRID_EV_UNKNOWN = 0
GRID_EV_BUP = 1
GRID_EV_BDOWN = 2

# ------------------------------------------------------------------------
class GridEvent:
    def __init__(self, event, x, y):
        self.event = event
        self.x = x
        self.y = y

# ------------------------------------------------------------------------
# Basic 8x8 grid - each half of amonome, no coordinates translation
class Grid8x8:

    def __init__(self, port, timeout):
        self.s = serial.Serial(port,
            baudrate = 115200,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = timeout,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False)
        self.s.flushInput()
        self.s.flushOutput()
        self.buf = []

    def close(self):
        self.s.flushInput()
        self.s.flushOutput()
        self.s.close()

    def reset(self):
        self.clear()
        self.led_test(0)
        self.intensity(15)

    def reboot(self):
        self.send([0xfa, 0xaf])

    def timeout(self, v):
        self.s.timeout = v

    def send(self, data):
        tosend = chr(data[0]) + chr(data[1])
        self.s.write(tosend)

    def led_test(self, state):
        data = [0x40, state]
        self.send(data)

    def intensity(self, value):
        data = [0x30, value]
        self.send(data)

    def led_row(self, row, coldata):
        data = [0x70 | row, coldata]
        self.send(data)

    def led_column(self, col, rowdata):
        data = [0x80 | col, rowdata]
        self.send(data)

    def shutdown(self, state):
        data = [0x60, state]
        self.send(data)

    def led(self, state, x, y):
        data = [0, 0]
        data[0] = 0x20 | state
        data[1] = (x<<4) | y
        self.send(data)

    def clear(self):
        for row in range(0,8):
            self.led_row(row, 0)

    def read(self):
        lbuf = self.s.read(2 - len(self.buf))
        for char in [ord(x) for x in lbuf]:
            self.buf.append(char)

        if len(self.buf) < 2:
            return None

        address = self.buf[0] >> 4;
        state = self.buf[0] & 0x0F
        data = self.buf[1]
        self.buf = []

        # button press/depress
        if address == 0:
            x = data >> 4;
            y = data & 0xF
            if state == 1:
                return GridEvent(GRID_EV_BDOWN, x, y)
            elif state == 0:
                return GridEvent(GRID_EV_BUP, x, y)
            else:
                return GridEvent(GRID_EV_UNKNOWN, x, y)
        else:
            return GridEvent(GRID_EV_UNKNOWN, x, y)

# ------------------------------------------------------------------------
class Screen:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.data = [[0 for x in xrange(self.height)] for x in xrange(self.width)]

    def set(self):
        self.data = [[1 for x in xrange(self.height)] for x in xrange(self.width)]

    def import_array(self, x, y, a):
        for l in range(0, len(a)):
            for c in range(0, len(a[0])):
                if x+c >= 0 and x+c < self.width and y+l >= 0 and y+l < self.height:
                    self.data[x+c][y+l] = a[l][c]

    def line_horiz(self, x, y, length):
        for xpos in range(x, x+length):
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                self.data[xpos][y] = 1

# ------------------------------------------------------------------------
# Full 8x16 grid with coordinates translation: (0,0) = upper left
class Amonome:

    def __init__(self, port0, port1, timeout):
        dtimeout = None
        if timeout is not None:
            dtimeout = timeout/2
        g0 = Grid8x8(port0, dtimeout)
        g1 = Grid8x8(port1, dtimeout)
        self.g = [g0, g1]

    def close(self):
        for g in self.g:
            g.close()

    def reset(self):
        for g in self.g:
            g.reset()

    def reboot(self):
        for g in self.g:
            g.reboot()

    def timeout(self, v):
        dtimeout = None
        if v is not None:
            dtimeout = v/2
        for g in self.g:
            g.timeout(dtimeout)

    def led(self, state, x, y):
        if x<8:
            self.g[0].led(state, 7-x, 7-y)
        else:
            self.g[1].led(state, x-8, y)

    def led_test(self, state):
        for g in self.g:
            g.led_test(state)

    def intensity(self, value):
        for g in self.g:
            g.intensity(value)

    def led_row(self, row, coldata):
        g0 = coldata >> 8
        g1 = int('{:08b}'.format(coldata &255)[::-1], 2)
        self.g[0].led_row(7-row, g0)
        self.g[1].led_row(row, g1)

    def led_column(self, col, rowdata):
        if col<8:
            self.g[0].led_column(7-col, rowdata)
        else:
            rowdata = int('{:08b}'.format(rowdata)[::-1], 2)
            self.g[1].led_column(col, rowdata)

    def shutdown(self, state):
        for g in self.g:
            g.shutdown()

    def clear(self):
        for g in self.g:
            g.clear()

    def anim_rows(self, frames):
        for f in frames:
            for l in f[1]:
                self.led_row(l[0], l[1])
            time.sleep(f[0])

    def anim_columns(self, frames):
        for f in frames:
            for l in f[1]:
                self.led_column(l[0], l[1])
            time.sleep(f[0])

    def blit(self, screen):
        if screen.width != 16 or screen.height != 8:
            raise TypeError("Cannot blit screens other than 16x8 onto amonome surface")
            return

        col_n = 0
        for column in screen.data:
            v = 0;
            for bit in column:
                v <<= 1
                v |= bit
            self.led_column(col_n, v);
            col_n += 1

    def read(self):
        ev = []

        for i in [0, 1]:
            evt = self.g[i].read()

            if evt is not None:
                if i == 0:
                    ev.append(GridEvent(evt.event, 7-evt.x, 7-evt.y))
                else:
                    ev.append(GridEvent(evt.event, evt.x+8, evt.y))

        return ev


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
