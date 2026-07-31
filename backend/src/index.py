import httpx
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from dependencies import limiter
from routes.todo import router as todo_router
from routes.accounts import router as accounts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
        app.state.http_client = client
        app.state.user_store = {}
        app.state.token_store = {}
        app.state.todo_store = {}
        yield

app = FastAPI(lifespan=lifespan)

app.include_router(accounts_router)
app.include_router(todo_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run("backend.src.index:app", host="0.0.0.0", port=8000, reload=True)