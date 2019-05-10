#!/usr/bin/env python

import sys
import pandas as pd
import numpy as nm


def data_preproc(pivot, measure, name):
    data = pd.read_csv("../ifloods_aoi.data")
    # seed,node,mean_aoi,mean_peak_aoi,strategy
    dd = data[data["graph"] == name]
    data_p = dd[dd["strategy"] == "plain"]
    data_t = dd[dd["strategy"] == "turbo"]
    rows = []
    for seed in set(dd[pivot]):
        part = data_p[data_p[pivot] == seed][measure]
        meanplain = part.mean()
        minplain = part.min()
        maxplain = part.max()
        plain10p = nm.percentile(part, 10)
        plain90p = nm.percentile(part, 90)

        part = data_t[data_t[pivot] == seed][measure]
        meanturbo = part.mean()
        minturbo = part.min()
        maxturbo = part.max()
        turbo10p = nm.percentile(part, 10)
        turbo90p = nm.percentile(part, 90)

        rows.append({"graph": name, pivot: seed, "minplain": minplain, "10pplain": plain10p, "meanplain": meanplain, "90pplain": plain90p, "maxplain": maxplain,
            "minturbo": minturbo, "10pturbo": turbo10p, "meanturbo": meanturbo, "90pturbo": turbo90p, "maxturbo": maxturbo})
    f = pd.DataFrame(rows)
    f.sort_values(by=["meanturbo"], inplace=True)
    f = f[::2]

    print(f"graph,seed,minplain,plain10p,meanplain,plain90p,maxplain,minturbo,turbo10p,meanturbo,turbo90p,maxturbo")
    for index, row in f.iterrows():
        print(f"{row['graph']},{row[pivot]},{row['minplain']},{row['10pplain']},{row['meanplain']},{row['90pplain']},{row['maxplain']},{row['minturbo']},{row['10pturbo']},{row['meanturbo']},{row['90pturbo']},{row['maxturbo']}")

if __name__ == "__main__":
    target = "sender"
    measure = "mean_aoi"
    name = "100_384_PL_0.edges"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    if len(sys.argv) > 2:
        measure = sys.argv[2]
    if len(sys.argv) > 3:
        measure = sys.argv[3]

    if target == "sender":
        data_preproc("seed", measure, name)
    elif target == "receiver":
        data_preproc("node", measure, name)
