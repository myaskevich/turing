
test:
	nosetests turing

sure:
	pip install mock nose parsimonious

clean:
	rm -f *.turc
	rm -fr dist/
	rm -fr build/
