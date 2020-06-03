clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

fmt:
	isort -rc .
	black .

verify:
	docker-compose up -d
	docker-compose run tests black --check --diff .
	docker-compose run tests pytest -vv --cov-report html --cov=sqlalchemy_filter tests/
	docker-compose down

build:
	docker-compose up -d --build
	docker-compose run tests black --check --diff .
	docker-compose run tests pytest -vv --cov-report xml --cov=sqlalchemy_filter tests/
	docker-compose run tests codecov -t c1131812-1766-49bf-9a4e-528bfca56625
	docker-compose down

publish:
	python setup.py sdist
	twine upload dist/*
