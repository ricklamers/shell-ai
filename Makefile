build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf build dist my_project.egg-info

publish: build
	twine upload dist/*

all: clean build publish

.PHONY: build clean publish
