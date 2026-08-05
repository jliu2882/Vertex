from typing import List, Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from schemas.tasks import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from services.tasks import verify_task_owner
from dependencies import requestLimiter, get_db, get_current_user_id

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get("", response_model=TaskListResponse)
@requestLimiter.limit("60/minute")
async def get_tasks(
    request: Request,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    q: Optional[str] = Query(None, min_length=1),
):
    query_filters = ""
    params = [current_user_id]

    if q:
        query_filters = " AND (title ILIKE $2 OR task_description ILIKE $2)"
        params.append(f"%{q}%")

    count_query = f"SELECT COUNT(*) FROM tasks WHERE user_id = $1{query_filters}"
    offset = (page - 1) * limit
    tasks_query = f"SELECT * FROM tasks WHERE user_id = $1{query_filters} ORDER BY id DESC LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}"

    try:
        total = await db.fetchval(count_query, *params)
        tasks = await db.fetch(tasks_query, *params, limit, offset)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch tasks")

    total = int(total or 0)
    total_pages = (total + limit - 1) // limit if total else 1

    return {
        "items": tasks,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    query = """
        INSERT INTO tasks (user_id, title, task_description) 
        VALUES ($1, $2, $3) 
        RETURNING id, user_id, title, task_description;
    """
    try:
        return await db.fetchrow(query, current_user_id, payload.title, payload.task_description)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create task")

@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    await verify_task_owner(db, task_id, current_user_id)
    query = """
        UPDATE tasks 
        SET 
            title = COALESCE($2, title),
            task_description = COALESCE($3, task_description)
        WHERE id = $1;
    """
    try:
        await db.execute(query, task_id, payload.title, payload.task_description)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update task")

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    await verify_task_owner(db, task_id, current_user_id)
    query = """
        DELETE FROM tasks WHERE id = $1;
    """
    try:
        await db.execute(query, task_id)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete task")