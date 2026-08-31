.PHONY: format lint

format:
	python -m black betacode/ tests/

lint:
	@failed=""; \
	run() { "$$@" || failed="$$failed\n  $$*"; }; \
	run python -m pylint betacode/ tests/; \
	run python -m black --check --quiet betacode/ tests/; \
	run codespell betacode/ tests/ --skip=tests/cases.py; \
	if [ -n "$$failed" ]; then \
		printf "\nFailed commands:%b\n" "$$failed"; \
		exit 1; \
	fi
