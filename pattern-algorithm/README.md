## Pattern Algorithms

### Run

#### Parallel

- Tomita, Tanaka, Takahashi _parallel_ version

```bash
 $ ./src/pattern-ttt-distr.py [--workers=NUM(CPUS) | --graph=PATH(null)]
```

- Pattabiraman, Gebremedhin, Liao, Choudhary _parallel_ version

```bash
 $ ./src/pattern-distr.py [--workers=NUM(CPUS) | --graph=PATH(null)]
```

- [_NX Python libray_](https://networkx.github.io/) iterative and parallel version

```bash
 $ ./src/pattern-nx-distr.py [--workers=NUM(CPUS) | --graph=PATH(null)]
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

```bash
 $ ./src/pattern-ttt-vertex.py [GRAPH_PATH]
```

- [_NX Python libray_](https://networkx.github.io/) iterative implementation of the above algorithm - [see](https://github.com/networkx/networkx/blob/master/networkx/algorithms/clique.py#L103)

```bash
 $ ./src/pattern-nx.py [GRAPH_PATH]
```

- _Map-Reduce_ implementation

```bash
 $ ./src/pattern-mr.py [GRAPH_PATH]
```

- Clean

```bash
 $ make clean
```

### Tests

- Download (_DIMACS_ benchmarks)

```bash
 $ make download
```

- _NX_ testing graphs

```bash
 $ make generate
```

- Clean

```bash
 $ make realclean
```

