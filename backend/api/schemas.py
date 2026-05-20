from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from models import PriorityEnum, AssigneeEnum, ColumnStatusEnum

# --- User Schemas ---
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    profileImageUrl: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CurrentUserResponse(BaseModel):
    user: UserResponse

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    assignee: AssigneeEnum
    columnStatus: Optional[ColumnStatusEnum] = ColumnStatusEnum.todo
    dueDate: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    assignee: Optional[AssigneeEnum] = None
    columnStatus: Optional[ColumnStatusEnum] = None
    dueDate: Optional[datetime] = None

class TaskMove(BaseModel):
    columnStatus: ColumnStatusEnum

class TaskResponse(TaskBase):
    id: str
    ticketNumber: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime
    userId: str

    model_config = ConfigDict(from_attributes=True)

class TaskStatsResponse(BaseModel):
    total: int
    todo: int
    inProgress: int
    inReview: int
    done: int

# --- Auth Schemas ---
class TokenResponse(BaseModel):
    token: str

# --- Health Schemas ---
class HealthResponse(BaseModel):
    status: str
