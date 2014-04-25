__author__ = 'atolmachev'
# coding=UTF-8

import Image as image
import math

def dist(r):
    return math.sqrt(r[0]*r[0] + r[1]*r[1])

def each_pair(arr, callback):
    for i in xrange(-1, len(arr)-1):
        callback(arr[i], arr[i+1])

def intergrate_pairwise(arr, callback):
    c = 0
    for i in xrange(-1, len(arr)-1):
        c += callback(arr[i], arr[i+1])
    return c

def move(p, dir) : return (p[0] + dir[0], p[1] + dir[1])

class Shape:
    def __init__(self, path):
        fp = open(path, "rb")
        self.im = image.open(fp)

    def mass_center(self):
        im = self.im
        xsum = ysum = cnt = 0
        for x in xrange(0, im.size[0]):
            for y in xrange(0, im.size[1]):
                if im.getpixel((x, y)) == 1:
                    xsum += x
                    ysum += y
                    cnt += 1
        return (xsum / cnt, ysum / cnt)

    def is_outer(self, p):
        im = self.im
        return p[0] < 0 or p[0] >= im.size[0] or \
               p[1] < 0 or p[1] >= im.size[1] or \
               im.getpixel((p[0], p[1])) == 255

    def is_inner(self, p): return not self.is_outer(p)

    def is_edge(self, p):
        return not self.is_outer(p) and \
               (self.is_outer((p[0]-1, p[1])) or self.is_outer((p[0]+1, p[1])) or \
               self.is_outer((p[0], p[1]-1)) or self.is_outer((p[0], p[1]+1)))

    def next_edge(self, p, circuit):
        dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for (dx, dy) in dirs:
            next = (p[0] + dx, p[1] + dy)
            if (not (next in circuit) and self.is_edge(next)): return next;
        return None

    def min_max_ratio(self):
        center = self.mass_center()
        im = self.im
        max_dist = 0
        min_dist = dist(im.size)
        for x in xrange(0, im.size[0]):
            for y in xrange(0, im.size[1]):
                if im.getpixel((x, y)) == 1 and self.is_edge((x, y)):
                    r = (abs(center[0] - x), abs(center[1] - y))
                    d = dist(r)
                    if d > max_dist: max_dist = d
                    if d < min_dist: min_dist = d
        #print "max_dist = %s, min_dist = %s" % (max_dist, min_dist)
        return (float(max_dist) / min_dist, max_dist, min_dist)

    def bound_square_ratio(self):
        (ratio, max, min) = self.min_max_ratio()
        center = self.mass_center()
        bound_square = 0
        fig_square = 0
        m = int(math.ceil(max))
        for x in xrange(center[0]- m, center[0]+ m):
            for y in xrange(center[1]- m, center[1]+ m):
                if (dist(((center[0]-x), (center[1]-y))) <= max):
                    bound_square += 1
                    if self.is_inner((x,y)): fig_square += 1
        return float(bound_square) / float(fig_square)

    def angle_number(self):
        center = self.mass_center()
        im = self.im
        start = None
        for x in xrange(0, center[0]):
            if self.is_edge((x, center[1])):
                start = (x, center[1])
                break
        next = start
        prev = None
        circuit_dists = []
        circuit = []
        while True:
            circuit.append(next)
            circuit_dists.append(dist((next[0]-center[0], next[1]-center[1])))
            temp = next
            next = self.next_edge(next, circuit)
            prev = temp
            if (next == None): break
        #print circuit
        #print circuit_dists
        growth = []
        each_pair(circuit_dists, lambda a, b: growth.append(b-a))
        angle_n = intergrate_pairwise(growth, lambda a, b: 1 if a*b<0 else 0)
        im = image.new('L', (self.im.size[0], self.im.size[1]), 'white')
        for p in circuit:
            im.putpixel(p, 1)
        im.save('circuit.BMP', 'BMP')

        return angle_n

if (__name__ == "__main__"):
    shape = Shape("C:\\Users\\atolmachev\\Documents\\kaggle\\tests\\triangle\\0_q1_30x30.BMP")
    print shape.bound_square_ratio()
