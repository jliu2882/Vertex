import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Request, status

from schemas.users import UserRegister, UserLogin
from services.users import generate_oauth2_token_response, hash_password, verify_password
from dependencies import requestLimiter, get_db

router = APIRouter(
    tags=["Users"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
@requestLimiter.limit("60/minute")
async def register_user(
    request: Request,
    payload: UserRegister, 
    db: asyncpg.Connection = Depends(get_db)
):
    query = """
        INSERT INTO users (email, username, password_hash) 
        VALUES ($1, $2, $3);
    """
    try:
        await db.execute(query, payload.email, payload.username, hash_password(payload.password))
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already registered")
    
    return generate_oauth2_token_response(payload.username)

@router.post("/login", status_code=status.HTTP_201_CREATED)
@requestLimiter.limit("60/minute")
async def login_user(
    request: Request,
    payload: UserLogin, 
    db: asyncpg.Connection = Depends(get_db)
):
    query = """
        SELECT username, password_hash FROM users WHERE email = $1
    """
    user = await db.fetchrow(query, payload.email)

    if (user is None or not verify_password(payload.password, user["password_hash"])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return generate_oauth2_token_response(user["username"])