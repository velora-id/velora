import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
    TITLE = "Velora AI Automation Agent"
    DESCRIPTION = "Platform AI agent & workflow automation berbasis Python + FastAPI + Firebase."
    HOST = "0.0.0.0"
    PORT = 8080
    RELOAD = False
