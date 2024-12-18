from map import *
import numpy as np
import math
import signal
import time
import typing

# Infinite cost represented by INF
INF = 9999


def euclidean_dist(x, y, z):
    x1, y1 = x
    x2, y2 = y
    z1, z2 = z
    
    if z1 != "variable" and z2 != "variable":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    else:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
