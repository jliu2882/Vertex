import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routes.tasks import router as tasks_router
from routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run("backend.src.index:app", host="0.0.0.0", port=8000, reload=True)