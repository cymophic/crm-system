from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="dev").lower().strip()

if ENVIRONMENT in ("production", "prod"):
    from .prod import *
elif ENVIRONMENT in ("development", "dev"):
    from .dev import *
else:
    raise ValueError(f"Invalid ENVIRONMENT='{ENVIRONMENT}'. Must be 'dev' or 'prod'.")
