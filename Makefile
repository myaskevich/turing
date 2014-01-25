
test:
	nosetests -s turing

sure:
	pip install mock nose parsimonious jinja2

clean:
	rm *.turc
