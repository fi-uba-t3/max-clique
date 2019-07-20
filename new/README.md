## New Algorithm

### Setup

- Dependencies: [venv](https://docs.python.org/3.6/library/venv.html)
 
```bash
$ python3 -m venv venv

$ source venv/bin/activate
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
```

### Run

#### Parallel

```bash
 $ ./src/new-distr.py [--workers=NUM(CPUS) | --graph=PATH(null)]
```

#### Secuencial

```bash
 $ ./src/new-iter.py [GRAPH_PATH]
```

- Clean

```bash
 $ ./clean.sh
```

### Tests

- All tests

```bash
 $ pytest
```

- Single test

```bash
 $ pytest FILE
```

