Makefile (Docker & Docs)
========================

Commandes prêtes à l’emploi pour **lancer la prod en local via Docker**, et **générer la doc**.

.. code-block:: makefile

   # --- Docker -------------------------------------------------
   IMAGE      := oc-lettings
   CONTAINER  := oc-lettings
   PORT       := 8000

   .PHONY: help build run stop rebuild logs

   help:
   	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) \
   	| awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

   build: ## Build de l’image Docker
   	docker build -t $(IMAGE) .

   run: ## Lance le conteneur
   	docker run -d --name $(CONTAINER) -p $(PORT):8000 $(IMAGE)

   stop: ## Stoppe & supprime le conteneur
   	-@docker rm -f $(CONTAINER) 2>/dev/null || true

   rebuild: build stop run ## Rebuild complet

   logs: ## Affiche les logs
   	docker logs -f $(CONTAINER)

   # --- Docs ---------------------------------------------------
   .PHONY: docs-html docs-serve docs-clean

   docs-html:
   	@$(MAKE) -C docs html

   docs-serve:
   	@$(MAKE) -C docs serve

   docs-clean:
   	@$(MAKE) -C docs clean
