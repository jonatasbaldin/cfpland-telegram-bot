dep-dev:
	pip install -r requirements-dev.txt

test:
	flake8 .

deploy-dev:
	npx sls deploy -s dev

deploy-prod:
	npm install
	npx sls deploy -s prod