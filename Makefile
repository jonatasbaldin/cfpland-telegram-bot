dep-dev:
	pip install -r requirements-dev.txt

test:
	flake8 .
	pytest

deploy-dev:
	sls deploy -s dev

deploy-prod:
	npm install
	sls deploy -s prod