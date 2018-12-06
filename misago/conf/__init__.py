from .gateway import settings, db_settings  # noqa

CACHE_NAME = "settings"

default_app_config = 'misago.conf.apps.MisagoConfConfig'


# Feature flag for easy changing between old and new settings mechanism
ENABLE_GLOBAL_STATE = True  # FIXME: delete after API changes