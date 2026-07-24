#(helper functions to check auth? idrk. data validation? idrk. error handling? idrk)

import httpx
from fastapi import Request

#SECRET_KEY = "your-todo-app-secret-key"
#ALGORITHM = "HS256"
#from fastapi.security import OAuth2PasswordBearer``
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
#from sqlalchemy.ext.asyncio import AsyncSession

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

async def get_db(request: Request):
    """
    take the request object from fastapi and yield a database session; have a finally to close db automatically
    
    async with request.app.state.db_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
    """
    return # not proper end but using as landmark for now

"""
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    should get db from previous function
    should get token should be obtained from oauth2_scheme (implemented from fastapi OAuth2PasswordBearer) which should get the user
        the token should be the one obtained from logging in or registering a user
        token should be decoded here and we check db if the user exists otherwise we toss the error

    returns the user for validation or smth (honestly return can be whatever we need for the implementation)
        uses can be getting user from the token we hold so we can filter items so users can only see their own todos
    returns an error [401?] if token is invalid for whatever (expired, modified/fake, deleted user/token)
"""