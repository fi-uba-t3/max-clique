PATH_GRAPHS = graphs

generate: 
	cd $(PATH_GRAPHS)
	./generate-graphs.py
	cd ..

clean:
	rm -rf __pycache__/

realclean: clean
	rm -f $(filter-out $(PATH_GRAPHS)/graph-small.txt $(PATH_GRAPHS)/graph-big.txt, $(wildcard $(PATH_GRAPHS)/*.txt))

.PHONY: generate clean realclean
