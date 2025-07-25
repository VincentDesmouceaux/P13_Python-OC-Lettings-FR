## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Surveillance & Logging

Nous utilisons Sentry pour capturer les erreurs en production :

1. Définir la variable d’environnement `SENTRY_DSN` (fourni par Sentry).
2. Le fichier `settings.py` initialise automatiquement Sentry si `SENTRY_DSN` est présent.
3. Les logs sont affichés en console (niveau DEBUG en dev, INFO/ERROR en prod).
4. Les exceptions non interceptées remontent dans Sentry grâce à l’intégration Django.

### Configuration requise

- `SENTRY_DSN` (env)
- Accès internet pour envoyer les événements à Sentry

### Étapes de déploiement

1. Exporter `SENTRY_DSN` sur le serveur.
2. Redémarrer l’application.  
3. Vérifier l’onglet « Issues » dans votre projet Sentry.

## Déploiement

### Aperçu du processus de déploiement

Le projet utilise une pipeline **CI/CD GitHub Actions** couplée à la plateforme **Northflank** pour automatiser le déploiement en production. À chaque push sur la branche principale (`master`/`main`), la suite suivante est exécutée :

1. **Tests & Linting**  
   - Lancement des tests unitaires (Pytest avec couverture > 80 %)  
   - Vérification de la qualité du code avec Flake8  
   Si une erreur survient, la pipeline s’arrête et empêche la suite du déploiement.

2. **Build de l’image Docker**  
   - Construction d’une image multi-architecture (amd64/arm64) à partir du `Dockerfile`.  
   - Injection de la variable `SENTRY_RELEASE=${GIT_SHA}` pour tracer la version.  
   - Push de l’image sur Docker Hub sous les tags `${DOCKER_REPO}:${IMAGE_TAG}` et `${DOCKER_REPO}:${GITHUB_SHA}`.

3. **Publication & Release**  
   - Notification d’une nouvelle release à Sentry (via `getsentry/action-release@v1`) pour centraliser le suivi des versions.

4. **Déploiement sur Northflank**  
   - Trigger d’un build via l’API Northflank (`POST /projects/${NF_PROJECT_ID}/services/${NF_OBJECT_ID}/build`).  
   - Northflank récupère l’image publiée et redéploie le conteneur.  
   - En fin de job, l’URL du service (ex. `https://<nom>-<projet>.code.run`) est affichée dans les logs.

> **Remarque**  
> - **DEV** (DEBUG=true) : les fichiers statiques sont servis depuis `static/`.  
> - **PROD** (DEBUG=false) : `manage.py collectstatic` génère `staticfiles/` servi par WhiteNoise (middleware activé automatiquement).

---

### Configuration requise

1. **Variables d’environnement de l’application** (`.env` ou équivalent)  
   Un fichier `.env.example` est fourni ci-dessous. Les variables essentielles :  
   - `DJANGO_DEBUG=false`  
   - `DJANGO_SECRET_KEY`  
   - `DJANGO_ALLOWED_HOSTS` (ex. `*.code.run`)  
   - `DJANGO_CSRF_TRUSTED_ORIGINS` (ex. `https://*.code.run`)  
   - `DJANGO_BEHIND_PROXY=true`  
   - `LOG_LEVEL=INFO`  
   - `WHITENOISE_MANIFEST_STRICT=false`  
   - `SENTRY_DSN` (+ `SENTRY_TRACES_SAMPLE`, optionnel)  
   - `PORT`, `PY_VER`, `DOCKER_REPO`, `IMAGE_TAG`  
   - Northflank : `NORTHFLANK_TOKEN`, `NF_PROJECT_ID`, `NF_OBJECT_ID`

2. **Secrets GitHub Actions**  
   Dans les Settings > Secrets du repo :  
   - `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`  
   - `DOCKER_REPO` / `IMAGE_TAG`  
   - `SENTRY_AUTH_TOKEN` / `SENTRY_ORG` / `SENTRY_PROJECT` / `SENTRY_URL`  
   - `NORTHFLANK_TOKEN` / `NF_PROJECT_ID` / `NF_OBJECT_ID`  
   - `PY_VER`

3. **Variables Northflank (service)**  
   Dans l’UI Northflank, configurez les mêmes variables d’application (**sans** CI-only tokens). Veillez à inclure `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`.

---

### Lien vers la documentation

  - https://p13-python-oc-lettings-fr-docs.readthedocs.io/fr/latest/index.html

