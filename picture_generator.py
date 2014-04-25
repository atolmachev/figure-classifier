import Image
import ImageDraw
import random as r
import os
import math
import shutil
from scipy.spatial import ConvexHull

data_path = os.path.dirname(os.path.abspath(__file__)) + '\\'

__author__ = 'viktor'
figures = ['rectangle', 'circle', 'triangle']
fig_numb = {'rectangle' : 1, 'circle' : 1, 'triangle' : 1}
minedge = 15

def f(im):
    return im

def area((x1, y1), (x2, y2)):
    return (x1*y2 - y1*x2)/2

def area3((x1, y1), (x2, y2), (x3, y3)):
    return abs(area( (x2-x1, y2-y1),
                     (x3-x1, y3-y1)))

def length((x1, y1), (x2, y2)):
    return ((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

def anglecos2((x1,y1), (x2,y2), (x3,y3)):
    return anglecos((x2-x1, y2-y1), (x3-x2, y3-y2))

def anglecos((x1,y1), (x2,y2)):
    return (x1*x2+y1*y2) / math.sqrt(x1*x1+y1*y1) / math.sqrt(x2*x2+y2*y2)
    
def invalid(pos, minanglecos):
    for i in range(0, len(pos)):
        for j in range(0, i):
            if (math.sqrt(length(pos[i], pos[j]))<minedge):
                return 1
    
    for i in range(0, len(pos)):
        if (anglecos2(pos[i-2], pos[i-1], pos[i]) > minanglecos):
            return 1
    return 0


def distort(w):
    return r.uniform(-w/2,w/2)

def makeRect(im):
    [x_size, y_size] = im.size
    draw = ImageDraw.Draw(im)
    
    minarea = x_size * y_size / 8
    pos = []
    edge = r.randint(minedge, min(x_size / 2, y_size / 2))
    angle = r.random() * math.pi / 2
    edgex = edge * math.cos(angle)
    edgey = edge * math.sin(angle)
    x0 = r.uniform(edgey, x_size - edgex)
    y0 = r.uniform(0, y_size - edgey - edgex)
    d = edge/6
    pos.append((x0 + distort(d), y0 + distort(d)))
    pos.append((x0+edgex+distort(d) , y0+edgey+distort(d)))
    pos.append((x0+edgex-edgey+distort(d), y0+edgey+edgex+distort(d)))
    pos.append((x0-edgey+distort(d), y0+edgex+distort(d)))
    draw.polygon(pos, 1)
    return im



def makeDisc(im):
    [x_size, y_size] = im.size
    draw = ImageDraw.Draw(im)
    x = (r.randint(0, x_size / 2), r.randint(0, y_size / 2))
    d = r.randint(min(x_size, y_size) / 3, min(x_size, y_size) / 2)
    y = (x[0] + d, x[1] + d)
    draw.ellipse((x, y), 1)
    return im

def makeTriangle(im):
    [x_size, y_size] = im.size
    draw = ImageDraw.Draw(im)
    minarea = x_size * y_size / 6
    while (1):
        ver = [(r.randint(0, x_size / 2), r.randint(0, y_size / 2)),
                (r.randint(x_size / 2, x_size), r.randint(y_size / 2, y_size)),
                (r.randint(x_size / 2, x_size), r.randint(0, y_size / 2)),
                (r.randint(0, x_size / 2), r.randint(y_size / 2, y_size))]
        del ver[r.randint(0, 3)]
        hull = ConvexHull(ver, False, 'QJ')
        ver = []
        for c in hull.vertices:
            ver.append((hull.points[c, 0], hull.points[c, 1]));
        if (invalid(ver, 0.8)):
            continue
        if (area3(ver[0], ver[1], ver[2]) > minarea):
            break

    draw.polygon(ver, 1)
    return(im)

def noise(im, level=1):
    if level == 1: return im

    [x_size, y_size] = im.size
    amount = min(x_size, y_size)*2
    draw = ImageDraw.Draw(im)

    if level == 2:
        pix = [(r.randint(1, x_size - 1), r.randint(1, y_size - 1)) for i in xrange(amount)]
        for i in pix:
            im.putpixel(i, abs(255 - im.getpixel(i)) )
        return im

    amount = min(x_size, y_size)*2
    mu = [(r.randint(1, x_size - 1), r.randint(1, y_size - 1)) for i in xrange(amount / 10)]
    sigma = (x_size / 6 / amount * 10 / 100, y_size / 6 / amount * 10 / 100)
    groups = [(int(r.gauss(mu[i][0], sigma[0])), int(r.gauss(mu[i][1], sigma[1]))) for j in xrange(amount) for i in xrange(amount / 10)]
    for i in groups:
        im.putpixel(i, abs(255 - im.getpixel(i)) )
    if level == 3: return im

    if level == 4:
        amount = min(x_size, y_size)
        #x_c = x_size / 30
        y_c = y_size / 13
        x_c = y_c
        for j in xrange(amount):
            x = (r.randint(1, x_size - 1), r.randint(1, y_size - 1))
            y = (r.randint(x[0] - x_c, x[0] + x_c), r.randint(x[1] - y_c, x[1] + y_c))
            draw.line((x, y))
        return im

    if level == 5:
        amount = r.randint(x_size / 2, x_size * 10)
        #x_c = x_size / 30
        y_c = y_size / 10
        x_c = y_c
        for j in xrange(amount):
            x = (r.randint(1, x_size - 1), r.randint(1, y_size - 1))
            y = (r.randint(x[0] - x_c, x[0] + x_c), r.randint(x[1] - y_c, x[1] + y_c))
            draw.line((x, y), abs(255 - im.getpixel(x)))
        return im

fig_func = {'rectangle' : makeRect, 'circle' : makeDisc, 'triangle' : makeTriangle}

def makeImages(quantity, quality=1, x_size=100, y_size=100, figures_to_draw=fig_numb, out_path=data_path):
    print "Producing data in " + out_path + '..'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for i in figures_to_draw.keys():
        fig_dir = out_path + str(i)
        #shutil.rmtree(fig_dir, True)
        if not os.path.exists(fig_dir):
                os.makedirs(fig_dir)
        for j in xrange(figures_to_draw[i] * quantity):
            im = Image.new('L', (x_size, y_size), 'white')
            im = fig_func[i](im)
            im = noise(im, quality)
            im.save(fig_dir + "\\" + str(j) + "_q" + str(quality) + '_' + str(x_size) + 'x' + str(y_size) + '.BMP', 'BMP')
    print "Done"