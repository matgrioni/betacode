build:
	python setup.py build

sdist:
	python setup.py sdist

publish:
	python setup.py sdist
	twine upload dist/*

publishtest:
	python setup.py sdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test:
	pytest

docs:
	pandoc --from=markdown --to=rst --output=README.rst README.md
	pandoc --from=markdown --to=plain --output=README README.md
	# Remove the first 3 lines of the README file which are badge related.
	sed -i 1,3d README

clean:
	if [ -d 'dist' ]; then \
		rm -r dist; \
	fi

	if [ -d 'build' ]; then \
		rm -r build; \
	fi
