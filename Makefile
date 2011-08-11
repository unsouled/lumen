SRC = src

all:
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf dist/ build/
	rm -f $(SRC)/Lumen/*.pyc
	rm -rf $(SRC)/Lumen.egg-info