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

style:
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run --no-deps web pep8 . --max-line-length=500
	$(DOCKER_COMPOSE) run --no-deps web pylint . -E --disable=E1002,E1101,E1102,E1103,E0203,E1003 --enable=C0111,W0613,W0611

clean:
	echo $$(docker stop $$(docker ps -a -q))
	echo $$(docker rm $$(docker ps -a -q))

test-web: clean
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run --rm web test web
