from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status

from dependencies import get_current_user, get_http_client, limiter
from schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


def _build_todo_response(todo: dict) -> TodoResponse:
    return TodoResponse(**todo)


def _find_user_todos(request: Request, owner_id: int) -> List[dict]:
    todo_store = request.app.state.todo_store
    return [todo for todo in todo_store.values() if todo["owner_id"] == owner_id]


@router.get("", response_model=List[TodoResponse])
@limiter.limit("60/minute")
async def get_my_todos(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    """
    Return todos belonging to the authenticated user.
    """
    return _find_user_todos(request, current_user["id"])


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
async def create_todo(
    request: Request,
    payload: TodoCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Create a todo item for the authenticated user.
    """
    todo_store = request.app.state.todo_store
    next_id = max(todo_store.keys(), default=0) + 1
    todo = {
        "id": next_id,
        "title": payload.title,
        "description": payload.description or "",
        "completed": False,
        "owner_id": current_user["id"],
    }
    todo_store[next_id] = todo
    return _build_todo_response(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
@limiter.limit("60/minute")
async def update_todo(
    todo_id: int,
    request: Request,
    payload: TodoUpdate,
    current_user: dict = Depends(get_current_user),
):
    """
    Update a todo item only if it belongs to the current user.
    """
    todo_store = request.app.state.todo_store
    todo = todo_store.get(todo_id)
    if not todo or todo["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if payload.title is not None:
        todo["title"] = payload.title
    if payload.description is not None:
        todo["description"] = payload.description
    if payload.completed is not None:
        todo["completed"] = payload.completed

    return _build_todo_response(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def delete_todo(
    todo_id: int,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a todo item for the authenticated user.
    """
    todo_store = request.app.state.todo_store
    todo = todo_store.get(todo_id)
    if not todo or todo["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    del todo_store[todo_id]
    return


@router.get("/external-data")
@limiter.limit("60/minute")
async def fetch_data(request: Request, client: httpx.AsyncClient = Depends(get_http_client)):
    """
    Example endpoint that demonstrates using the shared AsyncClient and rate limit.
    """
    return {"message": "TEST"}
