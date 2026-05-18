import os
from flask import redirect, make_response, request, jsonify
from database import SessionLocal
from models import Task, User, PriorityEnum, AssigneeEnum, ColumnStatusEnum
from auth import (
    get_current_user,
    create_session,
    delete_session,
    get_session_id,
    upsert_user,
    SESSION_COOKIE,
    SESSION_TTL_SECONDS,
    is_replit_environment,
    ISSUER_URL
)
from datetime import datetime

# Validador de sesión de usuario
def require_auth():
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401
    return user

def healthCheck():
    return {"status": "ok"}, 200

def getCurrentAuthUser():
    user = get_current_user()
    return {"user": user}, 200

def beginBrowserLogin(returnTo="/"):
    # Si OIDC real no está configurado, simulamos el inicio de sesión en local
    callback_url = f"/api/callback?code=mock_code&state=mock_state&returnTo={returnTo}"
    return redirect(callback_url)

def handleBrowserLoginCallback(code=None, state=None, iss=None, returnTo="/"):
    db = SessionLocal()
    try:
        # Reivindicaciones (claims) del usuario de desarrollo/mock
        claims = {
            "sub": "mock-user-123",
            "email": "admin@example.com",
            "first_name": "Marcelo",
            "last_name": "Guazzardo",
            "profile_image_url": "https://avatar.vercel.sh/marcelo"
        }
        
        db_user = upsert_user(db, claims)
        user_data = db_user.to_dict()
        
        # Crear sesión
        sid = create_session(
            db,
            user_data=user_data,
            access_token="mock_access_token",
            refresh_token="mock_refresh_token"
        )
        
        # Responder con la cookie de sesión y redirigir
        response = make_response(redirect(returnTo or "/"))
        response.set_cookie(
            SESSION_COOKIE,
            sid,
            max_age=SESSION_TTL_SECONDS,
            path="/",
            httponly=True,
            samesite="Lax",
            secure=False # Para compatibilidad de desarrollo sin HTTPS local
        )
        return response
    finally:
        db.close()

def logoutBrowserSession():
    sid = get_session_id()
    if sid:
        db = SessionLocal()
        try:
            delete_session(db, sid)
        finally:
            db.close()
            
    response = make_response(redirect("/"))
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response

def exchangeMobileAuthorizationCode(body):
    db = SessionLocal()
    try:
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
        return {"token": sid}, 200
    finally:
        db.close()

def logoutMobileSession():
    sid = get_session_id()
    if sid:
        db = SessionLocal()
        try:
            delete_session(db, sid)
        finally:
            db.close()
    return {"success": True}, 200

def listTasks(assignee=None, columnStatus=None):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        query = db.query(Task).filter(Task.userId == user["id"])
        
        if assignee:
            query = query.filter(Task.assignee == assignee)
        if columnStatus:
            query = query.filter(Task.columnStatus == columnStatus)
            
        tasks = query.order_by(Task.createdAt).all()
        return [t.to_dict() for t in tasks], 200
    finally:
        db.close()

def createTask(body):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        due_date = None
        if body.get("dueDate"):
            try:
                date_str = body["dueDate"].replace("Z", "+00:00")
                due_date = datetime.fromisoformat(date_str)
            except Exception:
                pass
                
        task = Task(
            title=body["title"],
            description=body.get("description"),
            priority=PriorityEnum(body["priority"]),
            assignee=AssigneeEnum(body["assignee"]),
            columnStatus=ColumnStatusEnum(body.get("columnStatus", "todo")),
            dueDate=due_date,
            userId=user["id"]
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.to_dict(), 201
    finally:
        db.close()

def getTaskStats():
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(Task.userId == user["id"]).all()
        stats = {
            "total": len(tasks),
            "todo": 0,
            "inProgress": 0,
            "inReview": 0,
            "done": 0
        }
        for t in tasks:
            status = t.columnStatus.value if hasattr(t.columnStatus, "value") else t.columnStatus
            if status == "todo":
                stats["todo"] += 1
            elif status == "in_progress":
                stats["inProgress"] += 1
            elif status == "in_review":
                stats["inReview"] += 1
            elif status == "done":
                stats["done"] += 1
        return stats, 200
    finally:
        db.close()

def getTask(id):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id, Task.userId == user["id"]).first()
        if not task:
            return {"error": "Task not found"}, 404
        return task.to_dict(), 200
    finally:
        db.close()

def updateTask(id, body):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id, Task.userId == user["id"]).first()
        if not task:
            return {"error": "Task not found"}, 404
            
        if "title" in body:
            task.title = body["title"]
        if "description" in body:
            task.description = body["description"]
        if "priority" in body:
            task.priority = PriorityEnum(body["priority"])
        if "assignee" in body:
            task.assignee = AssigneeEnum(body["assignee"])
        if "columnStatus" in body:
            task.columnStatus = ColumnStatusEnum(body["columnStatus"])
        if "dueDate" in body:
            due_date = None
            if body["dueDate"]:
                try:
                    date_str = body["dueDate"].replace("Z", "+00:00")
                    due_date = datetime.fromisoformat(date_str)
                except Exception:
                    pass
            task.dueDate = due_date
            
        task.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return task.to_dict(), 200
    finally:
        db.close()

def deleteTask(id):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id, Task.userId == user["id"]).first()
        if not task:
            return {"error": "Task not found"}, 404
            
        db.delete(task)
        db.commit()
        return "", 204
    finally:
        db.close()

def moveTask(id, body):
    auth_res = require_auth()
    if isinstance(auth_res, tuple):
        return auth_res
    user = auth_res
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == id, Task.userId == user["id"]).first()
        if not task:
            return {"error": "Task not found"}, 404
            
        task.columnStatus = ColumnStatusEnum(body["columnStatus"])
        task.updatedAt = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return task.to_dict(), 200
    finally:
        db.close()
