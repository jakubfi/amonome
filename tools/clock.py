#!/usr/bin/python

import sys
import amonome
import time

matrix = [[0 for x in xrange(8)] for x in xrange(16)]

digit = [
[
[ 1,1,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,1,1 ]
],
[
[ 0,1,0 ],
[ 1,1,0 ],
[ 0,1,0 ],
[ 0,1,0 ],
[ 0,1,0 ],
[ 1,1,1 ]
],
[
[ 1,1,1 ],
[ 0,0,1 ],
[ 1,1,1 ],
[ 1,0,0 ],
[ 1,0,0 ],
[ 1,1,1 ]
],
[
[ 1,1,1 ],
[ 0,0,1 ],
[ 0,1,1 ],
[ 0,0,1 ],
[ 0,0,1 ],
[ 1,1,1 ]
],
[
[ 1,0,0 ],
[ 1,0,0 ],
[ 1,0,1 ],
[ 1,1,1 ],
[ 0,0,1 ],
[ 0,0,1 ]
],
[
[ 1,1,1 ],
[ 1,0,0 ],
[ 1,1,1 ],
[ 0,0,1 ],
[ 0,0,1 ],
[ 1,1,1 ]
],
[
[ 1,1,1 ],
[ 1,0,0 ],
[ 1,1,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,1,1 ]
],
[
[ 1,1,1 ],
[ 0,0,1 ],
[ 0,1,0 ],
[ 0,1,0 ],
[ 0,1,0 ],
[ 0,1,0 ]
],
[
[ 1,1,1 ],
[ 1,0,1 ],
[ 1,1,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,1,1 ]
],
[
[ 1,1,1 ],
[ 1,0,1 ],
[ 1,0,1 ],
[ 1,1,1 ],
[ 0,0,1 ],
[ 1,1,1 ]
],
]

# ------------------------------------------------------------------------
def update(t, tsec, s):
    h1 = int(t.tm_hour/10)
    h2 = t.tm_hour % 10
    m1 = int(t.tm_min/10)
    m2 = t.tm_min % 10
    sec = t.tm_sec

    s.clear()
    if h1 > 0:
        s.import_array(0, 0, digit[h1])
    s.import_array(4, 0, digit[h2])
    s.import_array(9, 0, digit[m1])
    s.import_array(13, 0, digit[m2])
    if tsec % 2:
        s.line_horiz(0, 7, int(sec/3.75)+1)
    else:
        s.line_horiz(0, 7, int(sec/3.75))

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

tsec = 0
try:
    while True:
        now = time.localtime()
        update(now, tsec, s)
        g.blit(s)
        time.sleep(0.5)
        tsec += 1

except KeyboardInterrupt:
    print "Bye."

g.close()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
