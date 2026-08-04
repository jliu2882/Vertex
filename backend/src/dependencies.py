import os
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
import asyncpg

from slowapi import Limiter
from slowapi.util import get_remote_address

from services.users import decode_jwt_token

db_pool = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

requestLimiter = Limiter(key_func=get_remote_address)

async def get_db():
    """
    Add a paramater "db: asyncpg.Connection = Depends(get_db)," to allow access to an async connection to the database.

    Usage:
        db.fetchrow, db.fetch, db.fetchval, db.execute...
        db.fetchrow(query, [...])
    """
    global db_pool
    if db_pool is None:
        database_url = os.getenv("DATABASE_URL")
        db_pool = await asyncpg.create_pool(dsn=database_url)

    async with db_pool.acquire() as connection:
        yield connection

async def get_current_user_id(
    token: str = Depends(oauth2_scheme), 
    db: asyncpg.Connection = Depends(get_db)
):
    """Add a paramater "current_user_id: int = Depends(get_current_user_id)," to check current user against the task owner"""
    username = decode_jwt_token(token)
    query = """
        SELECT id FROM users WHERE username = $1
    """
    user = await db.fetchrow(query, username)
    return int(user["id"]) 