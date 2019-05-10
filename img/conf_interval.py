#!/bin/bash

import sys
import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats


def mean_confidence_interval(data, confidence=0.99):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h


if __name__ == "__main__":
    data = pd.read_csv(sys.argv[1])
    ind_var = (sys.argv[2])
    dep_var = (sys.argv[3])

    print("id,mean,leftint,rightint")
    for iv in sorted(set(data[ind_var])):
        part = data[data[ind_var] == iv]
        conf = mean_confidence_interval(np.array(part[dep_var]))
        print("{},{}".format(iv, ",".join([str(v) for v in conf])))
