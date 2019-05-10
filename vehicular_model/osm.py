#!/usr/bin/env python

# https://github.com/gboeing/osmnx-examples/blob/master/notebooks/01-overview-osmnx.ipynb

import osmnx as ox
import networkx as nx
import random
import middle
import matplotlib.pyplot as plt
import math
import numpy as nm
import os

location_point = (46.0585,11.1228)
ray = 1000


def download():
    G = ox.graph_from_point(location_point,
        distance=ray, distance_type='network', network_type='drive', simplify=False) 

    dir_path = os.path.dirname(os.path.realpath(__file__))
    ox.save_graphml(G, filename=dir_path+'/trento.graphml')
    fig, ax = ox.plot_graph(G, show=False, close=False)
    plt.savefig("trento.pdf")


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    inputs: x1, y1, x2, y2
    returns: distance in meters
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km*1000


def node_distance(n1, n2):
    y1 = n1['y']
    x1 = n1['x']
    y2 = n2['y']
    x2 = n2['x']
    return haversine(x1, y1, x2, y2)


def middle_point(n1, n2, d):
    y1 = n1['y']
    x1 = n1['x']
    y2 = n2['y']
    x2 = n2['x']
    (y, x) = middle.middle_2d_point(y1, x1, y2, x2, d)
    return {'y': y, 'x': x}

    
def close_nodes(G, node, ray):
    ray = abs(ray)
    nodes = []
    for n in G.nodes():
        v = G.nodes[n]
        if node_distance(node, v) < ray:
            nodes.append(n)
    return nodes


def sample_point(G):
    center = {'y': location_point[0], 'x': location_point[1]}
    dist = 500 #200 + abs(nm.random.normal(0, 0.25) * 800/2)  # let's assume gaussian is 0 in 5

    nodes = close_nodes(G, center, dist)
    H = G.subgraph(nodes)

    tot_len = street_len(H)

    v = random.random()
    dist = v*tot_len

    v_len = 0
    for e in H.edges:
        lanes = 2
        if 'lanes' in H.edges[e]:
            lanes = float(H.edges[e]['lanes'])
        elif H.edges[e]['oneway']:
            lanes = 1
        i = 0
        while v_len < dist and i < lanes:
            v_len += H.edges[e]['length']
            i += 1
        if v_len >= dist:
            break

    dist = v_len - dist # distance from end of the road to our point
    dist /= H.edges[e]['length']
    new_point = middle_point(H.nodes[e[1]], H.nodes[e[0]], dist)
    return new_point


def print_vehicles(G, V):
    H = ox.simplify_graph(G)
    fig, ax = ox.plot_graph(H, show=False, close=False)
    for v in V.nodes():
        ax.plot(V.nodes[v]['x'], V.nodes[v]['y'], marker='o', color='r')
    for s,t in V.edges():
        ax.plot([V.nodes[s]['x'],V.nodes[t]['x']], [V.nodes[s]['y'], V.nodes[t]['y']], color='r', linewidth=0.1)
    #plt.show()
    plt.savefig(f"trento_car_{len(V.nodes())}_{len(V.edges())}.pdf")


def v_graph(vehics, ray=300):
    G = nx.Graph()
    i = 0
    for v in vehics:
        G.add_node(i, x=v['x'], y=v['y'])
        for w in G.nodes():
            if i!=w and node_distance(G.nodes[i], G.nodes[w]) <= ray:
                G.add_edge(i, w)
        i += 1
    return G


def street_len(G):
    tot_len = 0
    for e in G.edges:
        lanes = 2.
        if 'lanes' in G.edges[e]:
            lanes = float(G.edges[e]['lanes'])
        elif G.edges[e]['oneway']:
            lanes = 1
        tot_len += (G.edges[e]['length'] * lanes)

    return tot_len


def sample_graph(G):
    vehicles = []

    for _ in range(100):
        vehicles.append( sample_point(G))
    H = v_graph(vehicles)

    #while not nx.is_connected(H):
    #    H = v_graph(vehicles)
    H = max(nx.connected_component_subgraphs(H), key=len)

    print_vehicles(G, H)
    return H


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    G = ox.load_graphml(dir_path+"/trento.graphml")
    H = sample_graph(G)
    nx.write_graphml(H, path=f"trento_car_{len(H.nodes())}_{len(H.edges())}.graphml")
    nx.write_weighted_edgelist(H, f"trento_car_{len(H.nodes())}_{len(H.edges())}.edges")
