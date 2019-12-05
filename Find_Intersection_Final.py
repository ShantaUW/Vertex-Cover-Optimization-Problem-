from math import sqrt

EPSILON = 0.001

def partly(a):
    if isinstance(a, float):


        return "{0:.2f}".format(a)
    return str(a)

class point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return '(' + partly(self.x) + ',' + partly(self.y) + ')'


class line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

def intersect (l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y

    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    xdifference = (x1 - x2, x3 - x4)
    ydifference = (y1 - y2, y3 - y4)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdifference, ydifference)
    if div == 0:
       return point(0, 0)

    d = (det([x1,y1],[x2,y2]), det([x3,y3],[x4,y4]))
    x = det(d, xdifference) / div
    y = det(d, ydifference) / div
    return point(x, y)


def findSlope(a,b):
    x1 = a.x
    x2 = b.x
    y1= a.y
    y2 = b.y
    if(x2==x1):
        return 1
    m = (y2-y1)/(x2-x1)
    return m


def findDistance(a,b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def is_Between(self, c):
        a, b = self.a, self.b
        cp = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(cp) > EPSILON:
            return False

        dp = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
        if dp < 0:
            return False

        squaredlength = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
        if dp > squaredlength:
            return False

        return True

def has_Intersect(l1,l2):
    if(Segment(l1.src, l1.dst).is_Between(l2.src) or Segment(l1.src, l1.dst).is_Between(l2.dst)):
        return True
    return False

def is_same_Line(l1,l2):
    if(findSlope(l1.src,l1.dst) == findSlope(l2.src,l2.dst) and has_Intersect(l1,l2)):
        return True
    return False

if __name__ == '__main__':
    pass

