DOCKER_COMPOSE?=docker-compose

build:
	$(DOCKER_COMPOSE) build

run-db:
	$(DOCKER_COMPOSE) up -d database

run:
	$(DOCKER_COMPOSE) up

server:
	$(DOCKER_COMPOSE) rm -f web
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) up web

clean:
	echo $$(docker stop $$(docker ps -a -q))
	echo $$(docker rm $$(docker ps -a -q))

test-web: clean
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run --rm web django-admin test web
