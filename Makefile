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
	docker-compose run tests codecov -t a005bdf5-4ab0-4b2a-91c8-8a99ad254d00
	docker-compose down

publish:
	python setup.py sdist
	twine upload dist/*
