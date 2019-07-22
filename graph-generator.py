#!/usr/bin/env python3

import os
import networkx as NX

PATH = "own-graphs"

os.mkdir(PATH)

seed = 100

# Erdos-Renyi
for prob in [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
    for size in [20, 40, 50, 70]:
        file_name = './{}/erdos_renyi_{}_{}_{}.txt'.format(PATH, size, prob, seed)
        G = NX.erdos_renyi_graph(size, prob, seed)
        NX.write_edgelist(G, file_name)
        seed += 1


for prob in [0.2, 0.4, 0.5, 0.6, 0.7]:
    for size in [100, 150, 200]:
        file_name = './{}/erdos_renyi_{}_{}_{}.txt'.format(PATH, size, prob, seed)
        G = NX.erdos_renyi_graph(size, prob, seed)
        NX.write_edgelist(G, file_name)
        seed += 1

# Duplication-divergence
for prob in [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
    for size in [20, 40, 50, 70, 100, 150, 200]:
        file_name = './{}/duplication_divergence_{}_{}_{}.txt'.format(PATH, size, prob, seed)
        G = NX.duplication_divergence_graph(size, prob, seed)
        NX.write_edgelist(G, file_name)
        seed += 1


# GNM
for size_to_edges in [lambda x: x // 2, lambda x: x, lambda x: x * 3 // 2]:
    for size in [20, 40, 50, 70, 100, 150, 200]:
        file_name = './{}/gnm_{}_{}_{}.txt'.format(PATH, size, size_to_edges(size), seed)
        G = NX.gnm_random_graph(size, size_to_edges(size), seed)
        NX.write_edgelist(G, file_name)
        seed += 1

for size_to_edges in [lambda x: x ** (3/2), lambda x: x ** 2 // 2]:
    for size in [20, 40, 50, 70]:
        file_name = './{}/gnm_{}_{}_{}.txt'.format(PATH, size, size_to_edges(size), seed)
        G = NX.gnm_random_graph(size, size_to_edges(size), seed)
        NX.write_edgelist(G, file_name)
        seed += 1


# Barbasi-Albert
for size_to_edges in [lambda x: x // 2, lambda x: x - 1, lambda x: x * 2 // 3]:
    for size in [20, 40, 50, 70, 100]:
        file_name = './{}/bar-alb_{}_{}_{}.txt'.format(PATH, size, size_to_edges(size), seed)
        G = NX.barabasi_albert_graph(size, size_to_edges(size), seed)
        NX.write_edgelist(G, file_name)
        seed += 1

# Powerlaw clustering
for prob in [0.2, 0.5, 0.9]:
    for size_to_edges in [lambda x: x // 2, lambda x: x - 1, lambda x: x * 2 // 3]:
        for size in [20, 40, 50, 70, 100, 150, 200]:
            file_name = './{}/powerlaw_cluster_{}_{}_{}_{}.txt'.format(PATH, size, size_to_edges(size), prob, seed)
            G = NX.powerlaw_cluster_graph(size, size_to_edges(size), prob, seed)
            NX.write_edgelist(G, file_name)
            seed += 1


# newman_watts_strogatz_graph
for k in [2, 5, 10, 19]:
    for size_to_edges in [lambda x: x // 2, lambda x: x, lambda x: x * 3 // 2]:
        for size in [20, 40, 50, 70, 100, 150, 200]:
            file_name = './{}/new_watts_stro_{}_{}_{}_{}.txt'.format(PATH, size, k, size_to_edges(size), seed)
            G = NX.newman_watts_strogatz_graph(size, k, size_to_edges(size), seed)
            NX.write_edgelist(G, file_name)
            seed += 1

for k in [2, 5, 10, 19]:
    for size_to_edges in [lambda x: x ** (3/2), lambda x: x ** 2 // 2]:
        for size in [20, 40, 50, 70]:
            file_name = './{}/new_watts_stro_{}_{}_{}_{}.txt'.format(PATH, size, k, size_to_edges(size), seed)
            G = NX.newman_watts_strogatz_graph(size, k, size_to_edges(size), seed)
            NX.write_edgelist(G, file_name)
            seed += 1
        
# watts_strogatz_graph
for k in [2, 5, 10, 19]:
    for size_to_edges in [lambda x: x // 2, lambda x: x, lambda x: x * 3 // 2]:
        for size in [20, 40, 50, 70, 100, 150, 200]:
            file_name = './{}/watts_stro_{}_{}_{}_{}.txt'.format(PATH, size, k, size_to_edges(size), seed)
            G = NX.watts_strogatz_graph(size, k, size_to_edges(size), seed)
            NX.write_edgelist(G, file_name)
            seed += 1

for k in [2, 5, 10, 19]:
    for size_to_edges in [lambda x: x ** (3/2), lambda x: x ** 2 // 2]:
        for size in [20, 40, 50, 70]:
            file_name = './{}/watts_stro_{}_{}_{}_{}.txt'.format(PATH, size, k, size_to_edges(size), seed)
            G = NX.watts_strogatz_graph(size, k, size_to_edges(size), seed)
            NX.write_edgelist(G, file_name)
            seed += 1
        
