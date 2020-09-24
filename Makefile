SRC = $(wildcard ./*.ipynb)

all: am4894bq docs

am4894bq: $(SRC)
	nbdev_build_lib
	touch am4894bq

build: $(SRC)
	nbdev_build_lib
	touch am4894bq

version: $(SRC)
	nbdev_bump_version

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist