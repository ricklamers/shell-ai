all: clean build publish

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf build dist my_project.egg-info

publish: build
	twine upload dist/*

.PHONY: build clean publish all
