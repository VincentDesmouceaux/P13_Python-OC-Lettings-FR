"""Expose le DSN Sentry au gabarit « base.html »."""
import os
from typing import Dict, Any


def sentry_dsn(_request) -> Dict[str, Any]:
    """Ajoute SENTRY_DSN au contexte global des templates."""
    return {"SENTRY_DSN": os.getenv("SENTRY_DSN")}
