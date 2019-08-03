dep-dev:
	pip install -r requirements-dev.txt

test:
	pytest

deploy-dev:
	sls deploy -s dev

deploy-prod:
	sls deploy -s prod

deploy-prod-ci:
	nvm install 11.9
  	npm install
	sls deploy -s prod
