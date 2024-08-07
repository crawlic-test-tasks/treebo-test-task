run:
	docker compose up --build

run-tests:
	docker compose up postgres redis --build -d
	pytest src/tests