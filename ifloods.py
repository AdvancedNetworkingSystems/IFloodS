#!/usr/bin/env python

import random
import os
import networkx as nx
import numpy as nm
import tandem_queue as tq
import matplotlib.pyplot as plt
import multiprocessing as mp


def optimize(A, turbo):
    n = A.shape[0]
    u = nm.ravel(nm.ones((n, 1)))
    d = nm.ravel(u.dot(A))
    M = A.dot(nm.linalg.inv(nm.diag(d)))
    if turbo:
        M = nm.transpose(M)
        t = nm.ravel(u.dot(M))
        M = M.dot(nm.linalg.inv(nm.diag(t)))
    else:
        t = u
    return (M, t)


def random_choice(n, probs):
    s = sum(probs)
    choice = None
    if s > 0:
        for i in range(n):
            probs[i] /= s
        choice = nm.random.choice(range(n), 1, p=probs)[0]
    return choice

def random_dest(A, j, smart_send):
    n = A.shape[0]
    choice = random_choice(n, nm.ravel(A[:, j]))
    if smart_send:
        A[choice, j] = 0
        A[j, choice] = 0
    return choice


def sending_attempt(e, f, seed):
    propagation_time = 1./100  # 1 hundredth of time cycle
    i, M, t, S, sched, alpha = e

    dest = random_dest(M, i, False)
    if S[dest] < S[i]:
        # print(f"{sched.elapsed_time()}: {i} sends to {dest}")
        sched.schedule_event(propagation_time, (-2,dest,S[i]))

    sched.schedule_event(1./(alpha*t[i]), (i, M, t, S, sched, alpha))


def spanning_tree(A, seed):
    n = A.shape[0]
    S1 = set([(None, seed)])
    S2 = set([seed])
    T = set()
    while len(S1) > 0:
        parent,node = S1.pop()
        S2.remove(node)
        for i in range(n):
            if A[i, node] > 0:
                if i in T or i in S2:
                    A[i, node] = 0
                else:
                    S1.add((node, i))
                    S2.add(i)
        if parent is not None:
            A[parent, node] = 1
        T.add(node)
    return optimize(A, False)


def simulate_flooding(G, dist, f, alpha=1, duration=100, lambdy=1, seed=None, name="culo"):
    A = nx.to_numpy_matrix(G)
    n = A.shape[0]
    if seed is None:
        seed = random.sample(range(n), 1)[0]
    if dist == "turbo":
        M, t = optimize(A, True)
    if dist == "plain":
        M, t = optimize(A, False)
    if dist == "tree":
        M, t = spanning_tree(A, seed)

    print(f"Simulating on {name}, {dist} distribution on graph with {n} nodes, seed {seed}")
    sched = tq.EventScheduler()
    S = {}

    for i in range(n):
        S[i] = 0  # last packet received timestamp
        sched.schedule_event(1./(alpha*t[i]), (i, M, t, S, sched, alpha))

    sched.schedule_event(lambdy, (-1,))

    while sched.elapsed_time() < duration:
        e = sched.pop_event()
        if e[0] == -1:
            S[seed] = sched.elapsed_time()
            sched.schedule_event(lambdy, (-1,))
        elif e[0] == -2:
            if S[e[1]] < e[2]:
                S[e[1]] = e[2]
                f.write(f"{seed},{sched.elapsed_time()},{e[1]},{S[e[1]]},{dist},{el}\n")
        else:
            sending_attempt(e, f, seed)

if __name__ == "__main__":
    duration = 100
    input_list = []
    pool = mp.Pool(8)
    with open("ifloods.data", "w") as f:
        f.write("seed,time,node,last_creat_ts,strategy,name\n")
        for folder in ["topos/"]:
            for el in os.listdir(folder):
                if el.endswith(".edges"):
                    G = nx.read_weighted_edgelist(folder + el)
                    n = len(G.nodes())
                    for seed in range(3): # random.sample(range(n), 10):
                        simulate_flooding(G, "turbo", f, seed=seed, duration=duration, name=el.split('.')[0])
                        simulate_flooding(G, "plain", f, seed=seed, duration=duration, name=el.split('.')[0])
