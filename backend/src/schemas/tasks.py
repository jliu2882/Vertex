from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    task_description: Optional[str] = Field(default="", max_length=5000)

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def handle_asyncpg_record(cls, data: Any) -> Any:
        if data is None:
            return data
        
        if type(data).__name__ == "Record": 
            return dict(data)
        return data

class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    page: int
    limit: int
    total: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    task_description: Optional[str] = Field(default=None, max_length=5000)