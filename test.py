__author__ = 'atolmachev'
# coding=UTF-8

import picture_generator as pg
import metrics
import os

class FigInfo:
    def __init__(self, file, ratio, max, min):
        self.file = file
        self.ratio = ratio
        self.max = max
        self.min = min

def map(l, callback):
    new_l = []
    for element in l:
       new_l.append(callback(element))
    return new_l

for s in xrange(30, 100, 30):
    pg.makeImages(100, 1, s, s)

types = ['rectangle', 'circle', 'triangle']
ranges = {}
fig_traceback = {}
for t in types:
    proportions = []
    square_ratios = []
    files = [f for f in os.listdir('./'+t) if os.path.isfile('./'+t+'//' + f)]
    for f in files:
        shape = metrics.Shape('./'+t+'//' + f)
        square_ratio = shape.bound_square_ratio()
        square_ratios.append(square_ratio)

    f2 = open(t+'-sq_ratios.csv', 'wb')
    f2.write(','.join(map(square_ratios, str)))
    f2.close()

