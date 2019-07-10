PATH_GRAPHS = graphs

download:
	# Downloads the testing graphs
	wget https://turing.cs.hbg.psu.edu/txn131/file_instances/clique/DIMACS_cliques.tar.gz
	tar xvf DIMACS_cliques.tar.gz
	# Downloads the converter: bin -> ascii
	# to format the graphs downloaded
	wget https://turing.cs.hbg.psu.edu/txn131/file_instances/converter.tar.gz
	tar xvf converter.tar.gz
	chmod +x converter/bin2asc
	# Applys the converter
	./convert.sh
	# Remove all the unnecessary lines
	# in graph´s files
	./transform.py
	rm graphs/*.clq
	# Clean the workspace
	rm -rf DIMACS_cliques DIMACS_cliques.tar.gz
	rm -rf converter converter.tar.gz

generate: 
	./$(PATH_GRAPHS)/generate-graphs.py
	mv *.txt $(PATH_GRAPHS)

clean:
	rm -rf src/__pycache__/

realclean: clean
	rm -f $(filter-out $(PATH_GRAPHS)/graph-small.txt $(PATH_GRAPHS)/graph-big.txt, $(wildcard $(PATH_GRAPHS)/*.txt))

.PHONY: generate clean realclean download
