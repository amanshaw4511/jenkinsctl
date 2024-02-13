build:
	rm -rf dist/*
	python -m build

deploy: build
	twine upload dist/*

deploy-local: build
	pip install dist/jenkinsctl*.whl --force-reinstall
