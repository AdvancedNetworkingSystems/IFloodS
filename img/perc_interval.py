#!/bin/bash

import sys
import pandas as pd
import numpy as nm


if __name__ == "__main__":
    data = pd.read_csv(sys.argv[1])
    ind_var = (sys.argv[2])
    dep_var = (sys.argv[3])

    print("id,min,perc10,mean,perc90,max")
    for iv in sorted(set(data[ind_var])):
        part = data[data[ind_var] == iv][dep_var]
        avg = part.mean()
        std = part.std()
        m = part.min()
        M = part.max()
        
        lp = nm.percentile(part, 10)
        rp = nm.percentile(part, 90)
        print(f"{iv},{m},{lp},{avg},{rp},{M}")
