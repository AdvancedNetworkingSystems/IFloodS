#!/usr/bin/env python

import sys


def upper_bound(n, prob=0.9999):
    p = 1./n
    k = 0
    while p < prob:
        k += 1
        p = 2*p - (3./2)*(p**2) + (p**3)/2
    print(f"{k}")


def upper_bound_cdf(n, prob=0.9999):
    p = 1./n
    k = 0
    dist = {k:p}
    while p < prob:
        k += 1
        p = 2*p - (3./2)*(p**2) + (p**3)/2
        dist[k] = p
    return dist


def upper_bound_dist(n, prob=0.9999):
    cdf = upper_bound_cdf(n, prob)
    dist = {}
    p = 0
    for k in cdf:
        dist[k] = cdf[k] - p
        p = cdf[k]
    return dist


if __name__ == "__main__":
    dist = upper_bound_dist(100)
    dist[0] = 0
    s = sum(dist.values())
    for k in dist:
        dist[k] /= s
    m = 0
    with open("omega_dist.data", "w") as filo:
        filo.write("k,p\n")
        for k in dist:
            m += k*dist[k]
            filo.write(f"{k},{dist[k]}\n")

    print(m)
    # upper_bound(float(sys.argv[1]))
