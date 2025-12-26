from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from starlette import status

from src.core.api_keys import get_organization_by_api_key
from src.core.firebase import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
api_key_header = APIKeyHeader(name="Authorization")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # In a real-world scenario, you would fetch the public key from a well-known URL
        # provided by your identity provider (e.g., Firebase Auth).
        # For this example, we'll use a placeholder.
        # You should replace this with your actual public key fetching logic.
        public_key = """-----BEGIN PUBLIC KEY-----
YOUR_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----"""
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="your-audience")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}


async def get_api_key(
    api_key: str = Depends(api_key_header), db=Depends(get_db)
) -> str:
    """
    Dependency that checks for a valid API key in the Authorization header.
    The key should be prefixed with "Bearer ".
    """
    if not api_key.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme.",
        )

    key = api_key.split(" ")[1]
    organization_id = get_organization_by_api_key(db, key)

    if not organization_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key.",
        )
    return organization_id
