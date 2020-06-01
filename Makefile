clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

code-style:
	black --check --diff .

fmt:
	black .

verify: code-style
verify:
	docker-compose up -d
	pytest -vv
	docker-compose down
