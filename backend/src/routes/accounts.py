import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status

from dependencies import get_current_user, limiter
from schemas import TokenResponse, UserLogin, UserRegister

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


def _hash_password(password: str) -> str:
    """
    Hash the password using SHA-256 for this demo.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _create_access_token() -> tuple[str, datetime]:
    """
    Create a bearer token and expiry timestamp.
    """
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)
    return token, expires_at


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
async def register_user(request: Request, payload: UserRegister):
    """
    Register a new user and store the credentials in-memory.
    """
    user_store = request.app.state.user_store
    normalized_email = payload.email.lower()
    if normalized_email in user_store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_id = max((user["id"] for user in user_store.values()), default=0) + 1
    user_store[normalized_email] = {
        "id": user_id,
        "email": normalized_email,
        "name": payload.name,
        "password_hash": _hash_password(payload.password),
    }
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("60/minute")
async def login_user(request: Request, payload: UserLogin):
    """
    Verify credentials and return an access token.
    """
    normalized_email = payload.email.lower()
    user = request.app.state.user_store.get(normalized_email)
    if not user or user["password_hash"] != _hash_password(payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token, expires_at = _create_access_token()
    request.app.state.token_store[token] = {"user": user, "expires_at": expires_at}
    return TokenResponse(access_token=token, token_type="bearer", expires_at=expires_at)


@router.get("/me")
@limiter.limit("60/minute")
async def read_current_user(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Return the currently authenticated user's public profile.
    """
    return {"id": current_user["id"], "email": current_user["email"], "name": current_user["name"]}
