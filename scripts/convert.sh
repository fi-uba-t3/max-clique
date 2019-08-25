#!/usr/bin/env bash

set -eu

for file in DIMACS_cliques/*; do
	./converter/bin2asc $file
done

mv DIMACS_cliques/*.clq graphs/

