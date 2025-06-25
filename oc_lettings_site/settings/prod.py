from .base import *  # noqa: F401,F403

DEBUG = False

# la variable MIDDLEWARE vient du `import *`
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    }
}
