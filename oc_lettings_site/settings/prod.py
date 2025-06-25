from .base import *  # noqa: F401,F403,F405

DEBUG = False

# la variable MIDDLEWARE provient du « import * »
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    }
}
