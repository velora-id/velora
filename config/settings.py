import os
from .development import DevelopmentConfig
from .staging import StagingConfig
from .production import ProductionConfig

config_by_name = dict(
    development=DevelopmentConfig,
    staging=StagingConfig,
    production=ProductionConfig
)

key = os.environ.get("APP_ENV", "development")
settings = config_by_name[key]()
