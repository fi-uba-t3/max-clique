URL_GRAPHS = https://turing.cs.hbg.psu.edu/txn131/file_instances
PATH_GRAPHS = graphs

PATTERN_PATH = pattern/$(PATH_GRAPHS)
NEW_PATH = new/$(PATH_GRAPHS)

GRAPHS = DIMACS_cliques
CONVERTER = converter

download:
	mkdir $(PATH_GRAPHS)
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
	rm $(PATH_GRAPHS)/*.clq
	# Move graphs to its folders
	cp $(PATH_GRAPHS)/* $(PATTERN_PATH)
	cp $(PATH_GRAPHS)/* $(NEW_PATH)
	# Clean the workspace
	rm -rf $(GRAPHS) $(GRAPHS).tar.gz
	rm -rf $(CONVERTER) $(CONVERTER).tar.gz
	rm -r $(PATH_GRAPHS)

clean:
	rm -f $(wildcard $(PATTERN_PATH)/*.txt)
	rm -f $(wildcard $(NEW_PATH)/*.txt)

.PHONY: clean download
