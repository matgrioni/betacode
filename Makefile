test:
	pytest

clean:
	rm dist/*
	rm build/*

publish:
	python setup.py sdist upload -r pypi
