import logging
import os
from django.apps import AppConfig
from django.template.loader import get_template

logger = logging.getLogger(__name__)


class OCLettingsSiteConfig(AppConfig):
    name = "oc_lettings_site"

    def ready(self):
        """
        Au démarrage du worker, on logge la date de modification
        d'un template représentatif pour vérifier que l'image
        contient bien les derniers fichiers HTML.
        """
        template_name = "lettings/index.html"
        try:
            tpl = get_template(template_name)
            mtime = os.path.getmtime(tpl.origin.name)
            logger.info(
                "Template %s chargé (mtime=%s)", template_name, mtime
            )
        except Exception as exc:  # pragma: no cover
            logger.warning("Template %s introuvable: %s", template_name, exc)
