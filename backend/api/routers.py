from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from database import SessionLocal
from models import Task, User, PriorityEnum, AssigneeEnum, ColumnStatusEnum
import schemas
from auth import (
    require_auth,
    get_current_user,
    get_db,
    upsert_user,
    create_session,
    delete_session,
    get_session_id,
    SESSION_COOKIE,
    SESSION_TTL_SECONDS
)

# ==============================================================================
# Routers
# ==============================================================================
root_router = APIRouter()
api_router = APIRouter()
auth_router = APIRouter()

# ==============================================================================
# Root & Health Endpoints
# ==============================================================================

@root_router.get("/health", response_model=schemas.HealthResponse)
def health_check():
    return {"status": "ok"}

# ==============================================================================
# Auth Endpoints
# ==============================================================================

@auth_router.get("/user", response_model=schemas.CurrentUserResponse)
def get_current_auth_user(user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user": user}

@auth_router.get("/login/browser")
def begin_browser_login(returnTo: str = "/"):
    callback_url = f"/api/auth/login/browser/callback?code=mock_code&state=mock_state&returnTo={returnTo}"
    return RedirectResponse(url=callback_url)

@auth_router.get("/login/browser/callback")
def handle_browser_login_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    code: Optional[str] = None,
    state: Optional[str] = None,
    iss: Optional[str] = None,
    returnTo: str = "/"
):
    claims = {
        "sub": "mock-user-123",
        "email": "admin@example.com",
        "first_name": "Marcelo",
        "last_name": "Guazzardo",
        "profile_image_url": "https://avatar.vercel.sh/marcelo"
    }
    
    db_user = upsert_user(db, claims)
    
    sid = create_session(
        db,
        user_data=db_user.to_dict(),
        access_token="mock_access_token",
        refresh_token="mock_refresh_token"
    )
    
    redirect_response = RedirectResponse(url=returnTo or "/", status_code=302)
    redirect_response.set_cookie(
        key=SESSION_COOKIE,
        value=sid,
        max_age=SESSION_TTL_SECONDS,
        path="/",
        httponly=True,
        samesite="lax",
        secure=False
    )
    return redirect_response

@auth_router.post("/logout/browser")
def logout_browser_session(request: Request, db: Session = Depends(get_db)):
    sid = get_session_id(request)
    if sid:
        delete_session(db, sid)
        
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response

@auth_router.post("/login/mobile", response_model=schemas.TokenResponse)
def exchange_mobile_authorization_code(request: Request, db: Session = Depends(get_db)):
    claims = {
        "sub": "mock-user-123",
        "email": "admin@example.com",
        "first_name": "Marcelo",
        "last_name": "Guazzardo",
        "profile_image_url": "https://avatar.vercel.sh/marcelo"
    }
    db_user = upsert_user(db, claims)
    sid = create_session(
        db,
        user_data=db_user.to_dict(),
        access_token="mock_access_token"
    )
    return {"token": sid}

@auth_router.post("/logout/mobile")
def logout_mobile_session(request: Request, db: Session = Depends(get_db)):
    sid = get_session_id(request)
    if sid:
        delete_session(db, sid)
    return {"success": True}

# ==============================================================================
# Tasks Endpoints
# ==============================================================================

@api_router.get("/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(
    assignee: Optional[str] = None,
    columnStatus: Optional[str] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    query = db.query(Task).filter(Task.userId == user["id"])
    
    if assignee:
        query = query.filter(Task.assignee == assignee)
    if columnStatus:
        query = query.filter(Task.columnStatus == columnStatus)
        
    tasks = query.order_by(Task.createdAt).all()
    return tasks

@api_router.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        assignee=task_in.assignee,
        columnStatus=task_in.columnStatus,
        dueDate=task_in.dueDate,
        userId=user["id"]
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@api_router.get("/tasks/stats", response_model=schemas.TaskStatsResponse)
def get_task_stats(
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    tasks = db.query(Task).filter(Task.userId == user["id"]).all()
    stats = {
        "total": len(tasks),
        "todo": 0,
        "inProgress": 0,
        "inReview": 0,
        "done": 0
    }
    for t in tasks:
        status_val = t.columnStatus.value if hasattr(t.columnStatus, "value") else t.columnStatus
        if status_val == "todo":
            stats["todo"] += 1
        elif status_val == "in_progress":
            stats["inProgress"] += 1
        elif status_val == "in_review":
            stats["inReview"] += 1
        elif status_val == "done":
            stats["done"] += 1
    return stats

@api_router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    task = db.query(Task).filter(Task.id == task_id, Task.userId == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@api_router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: str,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    task = db.query(Task).filter(Task.id == task_id, Task.userId == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
        
    task.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

@api_router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    task = db.query(Task).filter(Task.id == task_id, Task.userId == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete(task)
    db.commit()
    return Response(status_code=204)

@api_router.post("/tasks/{task_id}/move", response_model=schemas.TaskResponse)
def move_task(
    task_id: str,
    task_move: schemas.TaskMove,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    task = db.query(Task).filter(Task.id == task_id, Task.userId == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task.columnStatus = task_move.columnStatus
    task.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
