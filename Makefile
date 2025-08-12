###############################################################################
# Makefile – commandes développeur (sans secret en dur)
###############################################################################

SHELL := /bin/bash

# ----- Fichiers d'environnement -----
ENV_FILE ?= .env
SANITIZED_ENV := $(ENV_FILE).sanitized

# ----- Lecture d'une clé K dans $(ENV_FILE) sans sourcer le fichier -----
# - Ignore commentaires / lignes vides / décorations et coupe les commentaires inline
define dotenv
$(strip $(shell awk -F= -v k="$(1)" '
  /^[[:space:]]*#/      { next }                 # ignore commentaires
  /^[[:space:]]*$$/     { next }                 # ignore lignes vides
  !/=/{ next }                                   # ignore lignes sans "="
  { key=$$1; sub(/^[[:space:]]+|[[:space:]]+$$/,"",key) }
  key==k {
    val=$$0
    sub(/^[^=]*=[[:space:]]*/,"",val)            # retire la partie gauche + "="
    sub(/[[:space:]]*#.*/,"",val)                # coupe les commentaires inline
    sub(/^[[:space:]]+|[[:space:]]+$$/,"",val)   # trim
    print val; exit 0
  }
' "$(ENV_FILE)" 2>/dev/null))
endef

# ----- Variables dynamiques (ENV > .env > fallback) -----
# Port interne de l'app dans le conteneur (Gunicorn écoutera dessus)
APP_PORT := $(strip $(PORT))
ifeq ($(APP_PORT),)
  APP_PORT := $(strip $(call dotenv,PORT))
endif
ifeq ($(APP_PORT),)
  APP_PORT := 8000
endif

# Port hôte EXPOSÉ (figé par défaut à 8001)
HOST_PORT ?= 8001

# Références Docker locales
IMAGE      ?= oc-lettings
CONTAINER  ?= oc-lettings

# Image distante (seulement si DOCKER_REPO non vide)
DOCKER_REPO ?= $(call dotenv,DOCKER_REPO)
IMAGE_TAG   ?= $(call dotenv,IMAGE_TAG)
ifneq ($(strip $(DOCKER_REPO)),)
  REMOTE_IMAGE := $(strip $(DOCKER_REPO)):$(if $(strip $(IMAGE_TAG)),$(strip $(IMAGE_TAG)),latest)
endif

# SHA Git pour tagger la build
GIT_SHA := $(shell git rev-parse HEAD 2>/dev/null || echo dev)

# Garde-fou pour les cibles “remote”
define require_remote
	@if [ -z "$(strip $(DOCKER_REPO))" ]; then echo "❌ DOCKER_REPO manquant (définis-le dans l'environnement ou .env)"; exit 1; fi
endef

# ----- Sanitize .env pour docker run (ne garder que KEY=VALUE et #) -----
.PHONY: sanitize-env
sanitize-env:
	@if [ -f "$(ENV_FILE)" ]; then \
	  awk '\
	    /^[[:space:]]*#/ { print; next } \
	    /^[[:space:]]*$$/ { next } \
	    /^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=/ { print; next } \
	    { next }' "$(ENV_FILE)" > "$(SANITIZED_ENV)"; \
	  echo "→ Using sanitized env: $(SANITIZED_ENV)"; \
	fi

# ----------------------------------------------------------------------------- 
# Aide (cible par défaut)
# -----------------------------------------------------------------------------
.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ----------------------------------------------------------------------------- 
# Docker local
# -----------------------------------------------------------------------------
.PHONY: build
build: ## Build local (+ tag DOCKER_REPO:IMAGE_TAG s'il est défini)
	@if [ -n "$(REMOTE_IMAGE)" ]; then \
	  echo "→ docker build -t $(IMAGE) -t $(REMOTE_IMAGE)"; \
	  docker build --build-arg GIT_SHA=$(GIT_SHA) -t $(IMAGE) -t $(REMOTE_IMAGE) . ; \
	else \
	  echo "→ docker build -t $(IMAGE)"; \
	  docker build --build-arg GIT_SHA=$(GIT_SHA) -t $(IMAGE) . ; \
	fi

.PHONY: run
run: sanitize-env ## Lance le conteneur local (HOST $(HOST_PORT) → APP $(APP_PORT))
	@ENV_OPTS=""; \
	if [ -f "$(SANITIZED_ENV)" ]; then ENV_OPTS="--env-file $(SANITIZED_ENV)"; fi; \
	CP="$(APP_PORT)"; \
	if ! [[ "$$CP" =~ ^[0-9]+$$ ]]; then echo "⚠️  APP_PORT invalide ('$(APP_PORT)'), fallback 8000"; CP=8000; fi; \
	echo "→ docker run -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(IMAGE)"; \
	docker run -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(IMAGE)

.PHONY: stop
stop: ## Stoppe et supprime le conteneur s’il existe
	-@docker rm -f $(CONTAINER) 2>/dev/null || true

.PHONY: rebuild
rebuild: build stop run ## Rebuild complet : build → stop → run

.PHONY: logs
logs: ## Logs en continu (Ctrl-C pour sortir)
	docker logs -f $(CONTAINER)

# ----------------------------------------------------------------------------- 
# Docker Hub (images distantes)
# -----------------------------------------------------------------------------
.PHONY: pull
pull: ## Pull l'image distante (nécessite DOCKER_REPO ; tag=latest par défaut)
	$(call require_remote)
	docker pull $(REMOTE_IMAGE)

.PHONY: run-remote
run-remote: sanitize-env ## Lance depuis l'image distante (HOST $(HOST_PORT) → APP $(APP_PORT))
	$(call require_remote)
	@ENV_OPTS=""; \
	if [ -f "$(SANITIZED_ENV)" ]; then ENV_OPTS="--env-file $(SANITIZED_ENV)"; fi; \
	CP="$(APP_PORT)"; \
	if ! [[ "$$CP" =~ ^[0-9]+$$ ]]; then echo "⚠️  APP_PORT invalide ('$(APP_PORT)'), fallback 8000"; CP=8000; fi; \
	echo "→ docker run -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(REMOTE_IMAGE)"; \
	docker run -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(REMOTE_IMAGE)

.PHONY: up-remote
up-remote: stop pull run-remote ## Stop + pull + run-remote

.PHONY: run-remote-latest
run-remote-latest: sanitize-env ## Force un pull à chaque run (Docker récent)
	$(call require_remote)
	@ENV_OPTS=""; \
	if [ -f "$(SANITIZED_ENV)" ]; then ENV_OPTS="--env-file $(SANITIZED_ENV)"; fi; \
	CP="$(APP_PORT)"; \
	if ! [[ "$$CP" =~ ^[0-9]+$$ ]]; then echo "⚠️  APP_PORT invalide ('$(APP_PORT)'), fallback 8000"; CP=8000; fi; \
	echo "→ docker run --pull=always -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(REMOTE_IMAGE)"; \
	docker run --pull=always -d --name $(CONTAINER) -p $(HOST_PORT):$$CP $$ENV_OPTS $(REMOTE_IMAGE)

# ----------------------------------------------------------------------------- 
# Docs (Sphinx)
# -----------------------------------------------------------------------------
.PHONY: docs-html docs-serve docs-clean docs-linkcheck docs-doctest
docs-html:      ; @$(MAKE) -C docs html
docs-serve:     ; @$(MAKE) -C docs serve
docs-clean:     ; @$(MAKE) -C docs clean
docs-linkcheck: ; @$(MAKE) -C docs linkcheck
docs-doctest:   ; @$(MAKE) -C docs doctest
