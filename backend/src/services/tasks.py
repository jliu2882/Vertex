from fastapi import HTTPException, status
import asyncpg

async def verify_task_owner(db: asyncpg.Connection, task_id: int, user_id: int) -> None:
    """
    Usage:
        await verify_task_owner(db_connection, task_id_to_verify, current_user_id)
    """
    task = await db.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")