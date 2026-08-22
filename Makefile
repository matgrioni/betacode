.PHONY: format lint

format:
	python -m black betacode/ tests/

lint:
	python -m pylint betacode/ tests/
