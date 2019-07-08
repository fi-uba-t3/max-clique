PATH_GRAPHS = graphs

generate: 
	./$(PATH_GRAPHS)/generate-graphs.py
	mv *.txt $(PATH_GRAPHS)

clean:
	rm -rf __pycache__/

realclean: clean
	rm -f $(filter-out $(PATH_GRAPHS)/graph-small.txt $(PATH_GRAPHS)/graph-big.txt, $(wildcard $(PATH_GRAPHS)/*.txt))

.PHONY: generate clean realclean
