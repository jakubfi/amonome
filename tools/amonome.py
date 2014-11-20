import serial
import time
import random

class Grid:

    def __init__(self, port):
        self.s = serial.Serial(port,
            baudrate = 115200,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = 0.1,
            xonxoff = False,
            rtscts = False,
            dsrdtr = False)
        self.s.flushInput()
        self.s.flushOutput()
        self.matrix = [[0 for x in xrange(8)] for x in xrange(8)]

    def close(self):
        self.s.flushInput()
        self.s.flushOutput()
        self.s.close()

    def reset(self):
        self.leds_off()
        self.led_test(0)
        self.intensity(15)

    def reboot(self):
        self.send([0xfa, 0xaf])

    def send(self, data):
        tosend = chr(data[0]) + chr(data[1])
        print "Sending: 0x%02x, 0x%02x" % (data[0], data[1])
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
        print "led: %i x=%i, y=%i" % (state, x, y)
        data = [0, 0]
        data[0] = 0x20 | state
        data[1] = (x<<4) | y
        self.send(data)

    def leds_off(self):
        for row in range(0,8):
            self.led_row(row, 0)

    def read(self):
        if self.s.inWaiting() < 2:
            return

        data = [ord(x) for x in self.s.read(2)]
        print "Read: 0x%02x, 0x%02x" % (data[0], data[1])
        address = data[0] >> 4;

        # button press/depress
        if address == 0:
            state = data[0] & 0x0F
            x = data[1] >> 4;
            y = data[1] & 0xF
            if state == 1:
                if self.matrix[x][y] == 1:
                    self.led(0, x, y)
                    self.matrix[x][y] = 0
                else:
                    self.led(1, x, y)
                    self.matrix[x][y] = 1

class Amonome:

    def __init__(self, port0, port1):
        g0 = Grid(port0)
        g1 = Grid(port1)
        self.g = [g0, g1]

    def close(self):
        self.g[0].close()
        self.g[1].close()

    def reset(self):
        self.g[0].reset()
        self.g[1].reset()

    def reboot(self):
        self.g[0].reboot()
        self.g[1].reboot()

    def led(self, state, x, y):
        if x<8:
            self.g[0].led(state, 7-y, x)
        else:
            self.g[1].led(state, x-8, y)

    def led_test(self, state):
        self.g[0].led_test(state)
        self.g[1].led_test(state)

    def intensity(self, value):
        self.g[0].intensity(value)
        self.g[1].intensity(value)

    def led_row(self, row, coldata):
        g0 = int('{:08b}'.format(coldata >> 8)[::-1], 2)
        g1 = int('{:08b}'.format(coldata &255)[::-1], 2)
        self.g[0].led_column(7-row, g0)
        self.g[1].led_row(row, g1)

    def led_column(self, col, rowdata):
        if col<8:
            self.g[0].led_row(col, rowdata)
        else:
            rowdata = int('{:08b}'.format(rowdata)[::-1], 2)
            self.g[1].led_column(col, rowdata)

    def shutdown(self, state):
        self.g[0].shutdown()
        self.g[1].shutdown()

    def leds_off(self):
        self.g[0].leds_off()
        self.g[1].leds_off()

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

    def read(self):
        self.g[0].read()
        self.g[1].read()
