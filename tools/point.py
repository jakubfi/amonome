import math

# ------------------------------------------------------------------------
class Point:
# ------------------------------------------------------------------------

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%i, %i)" % (self.x, self.y)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def dist(self, other):
        return round(math.sqrt(pow((self.x-other.x), 2) + pow((self.y-other.y), 2)))
