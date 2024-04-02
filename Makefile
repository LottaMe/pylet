.PHONY: test
test:
	PYTHONPATH=./pylet pytest
run: 
	python pylet
setup: requirements.txt
	pip install -r requirements.txt
format:
	black . --extend-exclude exercises
	isort pylet