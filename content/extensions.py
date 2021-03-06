from flask_caching import Cache

from .ext.envconfig import EnvConfig
from .ext.apierrors import APIErrors
from .ext.applogging import AppLogging

envcfg = EnvConfig()
apierrors = APIErrors()
applogging = AppLogging()
cache = Cache()
