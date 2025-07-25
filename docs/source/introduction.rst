Introduction – Contexte & Mission
=================================

Orange County Lettings est en phase d’**hyper‑croissance**.  
Le produit fonctionne, mais la **codebase a besoin d’un grand ménage** : modularité,
qualité, déploiement, supervision. C’est là que vous intervenez.

Le pitch de Dominique (CTO)
---------------------------

> *« Bienvenue ! Tu as tout installé ? Parfait.  
> Maintenant, j’attends de toi :*  
> 
> - *une architecture Django modulaire (apps ``lettings`` & ``profiles``),*  
> - *du linting propre (sans changer la config),*  
> - *des tests > 80 % de couverture,*  
> - *un pipeline CI/CD (Docker → Northflank),*  
> - *du monitoring via Sentry,*  
> - *et une doc technique (Sphinx + Read the Docs) pour que la prochaine recrue se sente aussi bien que toi. »*

À la fin, tu devras **modifier le titre de la home**, **redéployer**, et **récupérer l’image Docker**
depuis Docker Hub : preuve que la chaîne est solide de bout en bout.

Objectifs de cette doc
----------------------

- Donner **les commandes essentielles** (pas de roman-fleuve).
- **Montrer le “pourquoi”** en plus du “comment”.
- Offrir un **parcours Prod-first** (le dev local = conteneur *prod-like*).
