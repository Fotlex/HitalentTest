ENV=prod

COMPOSE_FILE = docker/docker-compose.prod.yaml
ENV_FILE = .env
DOCKER_COMPOSE = docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE)
IP = 31.130.152.85

-include $(ENV_FILE)


.PHONY: build
build:
	@$(DOCKER_COMPOSE) build

.PHONY: up
up:
	@$(DOCKER_COMPOSE) up -d

.PHONY: up-logs
up-logs:
	@$(DOCKER_COMPOSE) up

.PHONY: logs
logs:
	@$(DOCKER_COMPOSE) logs -f

.PHONY: test
test:
	@$(DOCKER_COMPOSE) exec web pytest -v

.PHONY: down
down:
	@$(DOCKER_COMPOSE) down $(s)


.PHONY: restart
restart:
	@$(DOCKER_COMPOSE) restart


.PHONY: migrate
migrate:
	@echo "Running migrations for $(ENV) environment..."
	@$(DOCKER_COMPOSE) exec web python web/manage.py migrate --noinput

.PHONY: makemigrations
makemigrations:
	@$(DOCKER_COMPOSE) exec web python web/manage.py makemigrations $(APP)


.PHONY: collectstatic
collectstatic:
	@$(DOCKER_COMPOSE) exec web python web/manage.py collectstatic --noinput


.PHONY: base_commands
base_commands:
	@$(DOCKER_COMPOSE) exec web python web/manage.py migrate --noinput
	@$(DOCKER_COMPOSE) exec web python web/manage.py collectstatic --noinput
	@$(DOCKER_COMPOSE) exec web python web/manage.py createsuperuser


.PHONY: super_user
super_user:
	@$(DOCKER_COMPOSE) exec web python web/manage.py createsuperuser
