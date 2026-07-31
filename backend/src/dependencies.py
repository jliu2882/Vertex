from datetime import datetime

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")


def get_http_client(request: Request) -> httpx.AsyncClient:
    """
    Return the shared httpx AsyncClient instance from app state.
    """
    return request.app.state.http_client


async def get_db(request: Request):
    """
    Placeholder dependency for a database session.
    This can be expanded later with a real database connection.
    """
    yield None


async def get_current_user(token: str = Depends(oauth2_scheme), request: Request = None):
    """
    Authenticate requests using bearer tokens stored in app state.
    """
    token_store = getattr(request.app.state, "token_store", {})
    token_data = token_store.get(token)
    if not token_data or token_data["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data["user"]
