from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from firebase_admin import auth

from src.core.firebase import get_db
from src.core.security import get_current_user

router = APIRouter()

class UserRegistration(BaseModel):
    email: str
    password: str
    display_name: str

@router.post("/register")
async def register_user(user: UserRegistration):
    try:
        # Create user in Firebase Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.display_name
        )

        # Store user profile in Firestore
        db = get_db()
        doc_ref = db.collection(u'users').document(user_record.uid)
        doc_ref.set({
            u'email': user.email,
            u'display_name': user.display_name,
            u'created_at': user_record.user_metadata.creation_timestamp
        })

        return {"message": "User registered successfully", "uid": user_record.uid}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.get("/me")
async def get_current_user_details(current_user: dict = Depends(get_current_user)):
    db = get_db()
    doc_ref = db.collection(u'users').document(current_user['uid'])
    user_data = doc_ref.get().to_dict()
    return user_data