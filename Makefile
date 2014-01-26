
test:
	nosetests turing

sure:
	pip install mock nose parsimonious jinja2

clean:
	rm -f *.turc
	rm -fr dist/
	rm -fr build/
