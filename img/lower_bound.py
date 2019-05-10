#!/usr/bin/env python

import sys


def lower_bound(n, prob=0.9999):
    p = 1./n
    k = 0
    while p < prob:
        k += 1
        p = 2*p - (p**2)
    print(f"{k}")


if __name__ == "__main__":
    lower_bound(float(sys.argv[1]))
