
import firebase_admin
from firebase_admin import credentials, firestore, auth

def initialize_firebase():
    """Initializes the Firebase Admin SDK."""
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': cred.project_id,
    })

def get_db():
    """Returns the Firestore client."""
    return firestore.client()

def get_auth():
    """Returns the Firebase Auth client."""
    return auth
