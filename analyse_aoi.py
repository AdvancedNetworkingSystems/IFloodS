#!/usr/bin/env python

import pandas as pd


def analyse_aoi(duration):
    with open("ifloods_aoi.data", 'w') as f:
        f.write(f"seed,node,mean_aoi,mean_peak_aoi,strategy,graph\n")
        data = pd.read_csv("ifloods.data")
        for name in data['name'].unique():
            d0 = data[data['name'] == name]
            for seed in d0['seed'].unique():
                d1 = d0[d0['seed'] == seed]
                for strategy in ['turbo', 'plain']:
                    d2 = d1[d1['strategy'] == strategy]
                    for i in d2['node'].unique():
                        peak_aoi = []
                        dd = d2[d2['node'] == i]
                        u = 0  # last received pkt ts
                        k = 0  # last update time
                        ti =0  # time integral
                        for index, row in dd.iterrows():
                            ti += (row['time'] + k - 2*u)*(row['time']-k)/2
                            peak_aoi.append(row['time']-u)
                            u = row['last_creat_ts']
                            k = row['time']
                        ti += (duration + k - 2*u)*(duration-k)/2
                        peak_aoi.append(duration-u)

                        ti /= duration  # mean aoi for peer i
                        f.write(f"{seed},{i},{ti},{sum(peak_aoi)/len(peak_aoi)},{strategy},{name}\n")


if __name__ == "__main__":
    analyse_aoi(100)
