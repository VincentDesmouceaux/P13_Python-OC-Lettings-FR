# docs/Makefile
# =================
# Utilisation :
#   make -C docs html        # build HTML
#   make -C docs serve       # live-reload (nécessite sphinx-autobuild)
#   make -C docs linkcheck   # vérifier les liens externes
#   make -C docs doctest     # exécuter les doctests
#   make -C docs spelling    # vérif. orthographe (optionnel)
#   make -C docs clean       # nettoyer les artefacts de build

SPHINXBUILD     ?= sphinx-build
SPHINXAUTOBUILD ?= sphinx-autobuild
SOURCEDIR       = source
BUILDDIR        = build
SPHINXOPTS      ?= -W --keep-going -j auto

.PHONY: help html clean linkcheck doctest serve spelling

help:
	@$(SPHINXBUILD) -h

html:
	@$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html
	@echo
	@echo "✔ Les pages HTML sont dans $(BUILDDIR)/html"

clean:
	@rm -rf $(BUILDDIR)/*
	@echo "✔ Dossier $(BUILDDIR) vidé"

linkcheck:
	@$(SPHINXBUILD) -b linkcheck $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/linkcheck

doctest:
	@$(SPHINXBUILD) -b doctest $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/doctest

# Live reload (nécessite : pip install sphinx-autobuild)
serve:
	@$(SPHINXAUTOBUILD) $(SOURCEDIR) $(BUILDDIR)/html --open-browser

# Optionnel : nécessite sphinxcontrib-spelling + pyenchant
spelling:
	@$(SPHINXBUILD) -b spelling $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/spelling
