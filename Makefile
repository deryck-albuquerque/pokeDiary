IMAGE_NAME=pokeDiary

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker-compose up --build

up-d:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

rebuild:
	docker-compose down -v
	docker-compose up --build

run-api:
	python main.py

run-worker:
	python rabbit_worker.py