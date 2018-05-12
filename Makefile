build:
	python setup.py build

sdist:
	python setup.py sdist

publish:
	python setup.py sdist
	twine upload dist/*

test:
	pytest

clean:
	if [ -d 'dist' ]; then \
		rm dist/*; \
	fi

	if [ -d 'build' ]; then \
		rm build/*; \
	fi
