#!/usr/bin/env python
import math


def middle_2d_point(y1, x1, y2, x2, d):
    ''' d is the fraction of distance from x1, y1'''
    r2 = math.sqrt((y2-y1)**2+(x2-x1)**2)
    if y2-y1 > 0:
        ph2 = math.acos((x2-x1)/r2)
    else:
        ph2 = -math.acos((x2-x1)/r2)
    x3 = d*r2*math.cos(ph2)+x1
    y3 = d*r2*math.sin(ph2)+y1
    return (y3, x3)


if __name__ == "__main__":
    import random
    import matplotlib.pyplot as plt
    y1 = random.random()
    x1 = random.random()
    y2 = random.random()
    x2 = random.random()
    r2 = math.sqrt((y2-y1)**2+(x2-x1)**2)
    d = random.random()*r2
    (y3, x3) = middle_2d_point(y1, x1, y2, x2, d)
    plt.plot([x1, x3, x2], [y1, y3, y2])
    plt.plot(x1, y1, marker='o')
    plt.plot(x2, y2, marker='o')
    plt.plot(x3, y3, marker='o')
    plt.show()
