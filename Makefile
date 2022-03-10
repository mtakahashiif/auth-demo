##############################################################################
# Variables

COMPOSE_PROJECT_NAME=auth-demo

REALM_NAME := demo

REALM_FILE := $(REALM_NAME)-realm.json

EXPORTED_REALM_FILE := $(REALM_NAME)-realm-$(shell date +%s).json

# for keycloak container
export KEYCLOAK_IMPORT := /$(REALM_FILE)



##############################################################################
# Targets

.PHONY: build
build:
	$(MAKE) -C webapp build


.PHONY: up
up: up-keycloak
	sleep 30
	docker-compose up -d


.PHONY: stop
stop:
	@docker-compose stop


.PHONY: start
start:
	docker-compose start


.PHONY: restart
restart:
	docker-compose restart


.PHONY: down
down:
	@docker-compose down


.PHONY: up-keycloak
up-keycloak:
	docker-compose up --no-start keycloak
	docker cp $(REALM_FILE) $(COMPOSE_PROJECT_NAME)_keycloak_1:$(KEYCLOAK_IMPORT)
	docker-compose start keycloak


.PHONY: up-oauth2-proxy
up-oauth2-proxy:
	docker-compose up -d oauth2-proxy


.PHONY: up-webapp
up-webapp:
	docker-compose up -d webapp


.PHONY: stop-keycloak
stop-keycloak:
	docker-compose stop keycloak


.PHONY: stop-oauth2-proxy
stop-oauth2-proxy:
	docker-compose stop oauth2-proxy


.PHONY: stop-webapp
stop-webapp:
	docker-compose stop webapp


.PHONY: restart-keycloak
restart-keycloak:
	docker-compose stop keycloak
	docker-compose rm -f keycloak
	docker-compose up -d keycloak


.PHONY: restart-oauth2-proxy
restart-oauth2-proxy:
	docker-compose stop oauth2-proxy
	docker-compose rm -f oauth2-proxy
	docker-compose up -d oauth2-proxy


.PHONY: restart-webapp
restart-webapp:
	docker-compose stop webapp
	docker-compose rm -f webapp
	docker-compose up -d webapp


.PHONY: logs-keycloak
logs-keycloak:
	docker-compose logs -f keycloak


.PHONY: logs-oauth2-proxy
logs-oauth2-proxy:
	docker-compose logs -f oauth2-proxy


.PHONY: logs-webapp
logs-webapp:
	docker-compose logs -f webapp


# see
#   https://hub.docker.com/r/jboss/keycloak/
#   https://www.keycloak.org/docs/latest/server_admin/index.html#assembly-exporting-importing_server_administration_guide
.PHONY: export-realm
export-realm:
	docker exec -it $(COMPOSE_PROJECT_NAME)_keycloak_1 /opt/jboss/keycloak/bin/standalone.sh \
		-Djboss.socket.binding.port-offset=100 \
		-Dkeycloak.migration.action=export \
		-Dkeycloak.migration.provider=singleFile \
		-Dkeycloak.migration.realmName=$(REALM_NAME) \
		-Dkeycloak.migration.usersExportStrategy=REALM_FILE \
		-Dkeycloak.migration.file=/tmp/$(EXPORTED_REALM_FILE)

	docker cp $(COMPOSE_PROJECT_NAME)_keycloak_1:/tmp/$(EXPORTED_REALM_FILE) $(EXPORTED_REALM_FILE)