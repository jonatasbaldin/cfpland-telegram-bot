dep-dev:
	pip install -r requirements-dev.txt

test:
	pytest

deploy-dev:
	sls deploy -s dev

deploy-prod:
	sls deploy -s prod