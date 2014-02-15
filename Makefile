
test:
	nosetests turing

sure:
	pip install mock nose parsimonious

clean:
	rm -f *.turc
	rm -fr dist/
	rm -fr build/
	find . -name ".DS_Store" -print0 | xargs -0 rm -rf
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
