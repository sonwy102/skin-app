IMG_NAME ?= sonwy102/skin-app:v2
APP_NAME ?= web
DB_NAME ?= db
APP_CONTAINER ?= skin-app_web_1
DB_CONTAINER ?= skin-app_db_1

EXEC = docker exec -it $(APP_CONTAINER)
DB_EXEC = docker exec -it $(DB_CONTAINER)
SKIN_MANAGE = $(EXEC) python3 manage.py


BUILD_DIR = .

.PHONY: bash shell help build rebuild_app rebuild_db clean prune

help:
	@echo ''
	@echo 'Usage: make [TARGET] [ARGUMENTS]'
	@echo 'Targets:'
	@echo '  build    	build docker --image-- for current user: $(HOST_USER)(uid=$(HOST_UID))'

down:
	docker-compose down

up: start_db
	docker-compose up $(APP_NAME)

build: down
	docker build -t $(IMG_NAME) $(BUILD_DIR)

rebuild: build
	docker-compose up $(APP_NAME)

migrate: up
	$(SKIN_MANAGE) migrate

shell:
	$(SKIN_MANAGE) shell

bash:
	$(DB_EXEC) /bin/bash

load_product:
	$(SKIN_MANAGE) load_product

dump_db:
	$(SKIN_MANAGE) dumpdata product_search --indent=4 --natural-foreign --natural-primary

load_db:
	$(SKIN_MANAGE) loaddata product_search

stop_db:
	docker-compose down $(DB_NAME)

start_db:
	docker-compose up $(DB_NAME)

rebuild_db:
	$(SKIN_MANAGE) makemigrations
	$(SKIN_MANAGE) migrate

clean:
	docker-compose down -v --rmi all --remove-orphans

prune:
	docker system prune

test:
	# here it is useful to add your own customised tests
	docker-compose -it $(PROJECT_NAME)_$(HOST_UID) run --rm $(SERVICE_TARGET) sh -c '\
		echo "I am `whoami`. My uid is `id -u`." && echo "Docker runs!"' \
	&& echo success
