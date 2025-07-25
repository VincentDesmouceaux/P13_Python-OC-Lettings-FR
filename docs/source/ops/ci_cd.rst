CI / CD (GitHub Actions → Docker → Northflank)
==============================================

Pipeline (3 jobs)
-----------------

1. **🧪 Tests & Linting**
   - Installe les dépendances
   - **flake8** + **pytest** (couverture ≥ 80 %)
   - Upload des artefacts (coverage, flake8-report)

2. **🐋 Build & Push Docker + Release Sentry** *(master/main uniquement)*
   - Build multi‑arch (**linux/amd64, linux/arm64**)
   - Push sur **Docker Hub**
   - Création d’une **release Sentry** taggée avec le SHA

3. **🚀 Deploy on Northflank**
   - Appel API Northflank pour **déclencher le build & déploiement**
   - URL de prod affichée en fin de job

Secrets requis (GitHub)
-----------------------

- **PY_VER**
- **DOCKERHUB_USERNAME**, **DOCKERHUB_TOKEN**
- **DOCKER_REPO**, **IMAGE_TAG**
- **SENTRY_AUTH_TOKEN**, **SENTRY_ORG**, **SENTRY_PROJECT**, **SENTRY_URL**
- **NORTHFLANK_TOKEN**, **NF_PROJECT_ID**, **NF_OBJECT_ID**

Release & traçabilité
---------------------

- Le SHA Git est injecté dans l’image en **`SENTRY_RELEASE`** (ARG → ENV).
- Sentry peut ainsi **lier erreurs & release**.
