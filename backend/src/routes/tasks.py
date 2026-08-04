from typing import List

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Request, status

from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from services.tasks import verify_task_owner
from dependencies import requestLimiter, get_db, get_current_user_id

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.get("", response_model=List[TaskResponse])
@requestLimiter.limit("60/minute")
async def get_tasks(
    request: Request,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    # update query to implement search later
    #- get tasks (todos?page=1%limit=10%qParamsOpt=xyz) unauthen if not auth (pass page, limit, searchParams[opt]; return data, page, limit, totalPage)
    #filters/sort can be abc, time, letters for in task(too extra i think)
    query = """
        SELECT * FROM tasks WHERE user_id = $1
    """
    tasks = await db.fetch(query, current_user_id)

    for task in tasks:
        print(task['id'], task['name'])

    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    db: asyncpg.Connection = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    query = """
        INSERT INTO tasks (user_id, title, task_description) 
        VALUES ($1, $2, $3) 
        RETURNING id, title, task_description;
    """
    return await db.fetchrow(query, current_user_id, payload.title, payload.task_description)

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
    await db.execute(query, task_id, payload.title, payload.task_description)

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
    await db.execute(query, task_id)