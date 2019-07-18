URL_GRAPHS = https://turing.cs.hbg.psu.edu/txn131/file_instances
PATH_GRAPHS = graphs

GRAPHS = DIMACS_cliques
CONVERTER = converter

download:
	# Downloads the testing graphs
	wget $(URL_GRAPHS)/clique/$(GRAPHS).tar.gz
	tar xvf $(GRAPHS).tar.gz
	# Downloads the converter: bin -> ascii
	# to format the graphs downloaded
	wget $(URL_GRAPHS)/$(CONVERTER).tar.gz
	tar xvf $(CONVERTER).tar.gz
	chmod +x $(CONVERTER)/bin2asc
	# Applys the converter
	./convert.sh
	# Remove all the unnecessary lines
	# in graph´s files
	./transform.py
	rm graphs/*.clq
	# Clean the workspace
	rm -rf $(GRAPHS) $(GRAPHS).tar.gz
	rm -rf $(CONVERTER) $(CONVERTER).tar.gz

generate: 
	./$(PATH_GRAPHS)/generate-graphs.py
	mv *.txt $(PATH_GRAPHS)

clean:
	rm -rf src/__pycache__/

realclean: clean
	rm -f $(filter-out $(PATH_GRAPHS)/graph-small.txt $(PATH_GRAPHS)/graph-big.txt, $(wildcard $(PATH_GRAPHS)/*.txt))

.PHONY: generate clean realclean download
