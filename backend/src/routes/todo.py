# todolist.py (if user is authorized, endpoints to create/read/update/delete todos include filtering/pagination/sorting)
import httpx
from fastapi import APIRouter, Depends

from index import limiter
from dependencies import get_http_client

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("/external-data") #localhost/todos/external-data
@limiter.limit("5/minute")
async def fetch_data(client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get(
        "api_url + params as needed.com",
        params={
            "key": "key",
            "unitGroup": "us",
            "include": "current",
        }
    )
    return response.json()

"""
@router.get("/todos")
async def get_my_todos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Security and DB connection are completely handled above.
    # We just fetch todos belonging strictly to the logged-in user.
    return await db.scalars(select(Todo).where(Todo.user_id == current_user.id))
"""
