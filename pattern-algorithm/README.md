# Pattern Algorithms

Distributed algorithms for NP-complete MCP - Maximum Clique Problem

### Download

```bash
 $ make download
```

### Run

#### Parallel

```bash
 $ ./src/pattern-distr.py [--workers=NUM(CPUS) | --graph=PATH(null)]
```

#### Secuencial

- Bharath Pattabiraman, Assefaw H. Gebremedhin, Wei-keng Liao, Alok Choudhary - [see](https://arxiv.org/abs/1209.5818)

```bash
 $ ./src/pattern-recur.py [GRAPH_PATH]
```

- Etsuji Tomita, Akira Tanaka, Haruhisa Takahashi - [see](https://doi.org/10.1016/j.tcs.2006.06.015)

```bash
 $ ./src/pattern-ttt.py [GRAPH_PATH]
```

- [_NX Python libray_](https://networkx.github.io/) iterative implementation of the above algorithm - [see](https://github.com/networkx/networkx/blob/master/networkx/algorithms/clique.py#L103)

```bash
 $ ./src/pattern-nx.py [GRAPH_PATH]
```

```bash
 $ ./src/pattern-mr.py [GRAPH_PATH]
```

- Clean

```bash
 $ make clean
```

### Tests

```bash
 $ make generate
```

- Clean

```bash
 $ make realclean
```

