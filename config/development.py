from .base import Config

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8000
    RELOAD = True
