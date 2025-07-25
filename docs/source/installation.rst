Installation
============

Prérequis
---------

- Python 3.12+
- pip / venv
- (Optionnel) PostgreSQL 14+
- (Optionnel) Node.js si vous avez des outils front (non requis ici)

Étapes
------

1. **Cloner le dépôt** ::

      git clone <URL_REPO>
      cd P13_Python-OC-Lettings-FR

2. **Créer et activer l’environnement virtuel** ::

      python -m venv venv
      source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Installer les dépendances** ::

      pip install -r requirements.txt

4. **Configurer les variables d’environnement**  
   Copiez ``.env.example`` vers ``.env`` et adaptez les valeurs (voir :doc:`ops/settings`).

5. **Initialiser la base et lancer le serveur** ::

      python manage.py migrate
      python manage.py runserver

6. **(Optionnel) Lancer les tests** ::

      pytest -q

Installation de la documentation
--------------------------------

::

   pip install -r docs/requirements.txt
   make -C docs html
   open docs/build/html/index.html  # macOS (Linux: xdg-open)
