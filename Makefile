DOCKER_COMPOSE?=docker-compose


run-db:
	$(DOCKER_COMPOSE) up -d database

server: run-db
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run web python database.py
	$(DOCKER_COMPOSE) up web

style:
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run --no-deps web pep8 . --max-line-length=500
	$(DOCKER_COMPOSE) run --no-deps web pylint . -E --disable=E1002,E1101,E1102,E1103,E0203,E1003 --enable=C0111,W0613,W0611

test: style
	$(DOCKER_COMPOSE) run --rm web python tests.py

clean:
	echo $$(docker stop $$(docker ps -a -q))
	echo $$(docker rm $$(docker ps -a -q))

fixtures: clean
	$(DOCKER_COMPOSE) build web
	$(DOCKER_COMPOSE) run web python -c "import database; database.create_fixtures()"
	docker cp $$(docker ps -aqf "name=web"):/app/fixtures ./web/
