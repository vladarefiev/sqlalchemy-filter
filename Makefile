clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

fmt:
	black .

verify:
	docker-compose up -d --build
	docker-compose run tests black --check --diff .
	docker-compose run tests pytest -vv
	docker-compose down
