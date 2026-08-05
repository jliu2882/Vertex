import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import bcrypt
from fastapi import HTTPException, status

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
TOKEN_EXPIRY_MINUTES = int(os.getenv("JWT_TOKEN_EXPIRE_MINUTES"))

#region password encryptio/decryption logic
def hash_password(password: str) -> str:
    """Hash a plaintext password for storing in the database."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a stored hash."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
#endregion

#region token logic
def create_jwt_token(username: str) -> str:
    """Generates a secure JSON Web Token (JWT) string."""
    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token: str) -> str:
    """Decodes a JWT token and returns the username."""
    if SECRET_KEY is None or ALGORITHM is None:
        raise RuntimeError("JWT_SECRET_KEY and JWT_ALGORITHM must be configured")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception

    username = payload.get("username")
    if not username:
        raise credentials_exception

    return username

def generate_oauth2_token_response(username: str) -> Dict[str, Any]:
    """
    Helper function that returns the exact dict format expected by OAuth2
    and automated tools like FastAPI's Swagger UI.
    """
    return {
        "access_token": create_jwt_token(username),
        "token_type": "bearer"
    }
#endregion