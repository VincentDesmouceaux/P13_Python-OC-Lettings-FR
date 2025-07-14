###############################################################################
# Makefile – commandes développeur
#
# Objectif : simplifier les opérations locales courantes
# ─────────────────────────────────────────────────────────────────────────────
# • build        : construit l’image Docker « oc-lettings »
# • run          : lance un conteneur détaché sur le port 8000
# • stop         : arrête et supprime le conteneur si présent
# • rebuild      : build + stop + run            (équivalent à “docker compose up --build”)
# • logs         : affiche les logs du conteneur en continu
# • help (par défaut) : liste cette aide
###############################################################################

IMAGE      := oc-lettings
CONTAINER  := oc-lettings
PORT       := 8000

# ----------------------------------------------------------------------------- 
# CIBLE PAR DÉFAUT  →  affiche l’aide
# -----------------------------------------------------------------------------
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

# ----------------------------------------------------------------------------- 
# Construction de l’image
# -----------------------------------------------------------------------------
.PHONY: build
build: ## Build de l’image Docker
	docker build -t $(IMAGE) .

# ----------------------------------------------------------------------------- 
# Exécution du conteneur (détaché)
# -----------------------------------------------------------------------------
.PHONY: run
run: ## Lance le conteneur en détaché (port 8000)
	docker run -d --name $(CONTAINER) -p $(PORT):8000 $(IMAGE)

# ----------------------------------------------------------------------------- 
# Arrêt + suppression du conteneur s’il existe
# -----------------------------------------------------------------------------
.PHONY: stop
stop: ## Stoppe et supprime le conteneur
	-@docker rm -f $(CONTAINER) 2>/dev/null || true

# ----------------------------------------------------------------------------- 
# Rebuild complet : build → stop → run
# -----------------------------------------------------------------------------
.PHONY: rebuild
rebuild: build stop run ## Reconstruit puis relance le conteneur

# ----------------------------------------------------------------------------- 
# Logs “live” du conteneur
# -----------------------------------------------------------------------------
.PHONY: logs
logs: ## Affiche les logs en continu (Ctrl-C pour sortir)
	docker logs -f $(CONTAINER)
