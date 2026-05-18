import os
import secrets
from datetime import datetime, timedelta
import requests
from flask import request, make_response, redirect
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Session as DBSession, User as DBUser

SESSION_COOKIE = "sid"
SESSION_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 días
OIDC_COOKIE_TTL_SECONDS = 10 * 60      # 10 minutos
ISSUER_URL = os.environ.get("ISSUER_URL", "https://replit.com/oidc")

def get_session_id():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    return request.cookies.get(SESSION_COOKIE)

def get_session(db: Session, sid: str):
    row = db.query(DBSession).filter(DBSession.sid == sid).first()
    if not row:
        return None
    if row.expire < datetime.utcnow():
        db.delete(row)
        db.commit()
        return None
    return row.sess

def create_session(db: Session, user_data: dict, access_token: str, refresh_token: str = None, expires_at: int = None) -> str:
    sid = secrets.token_hex(32)
    session_data = {
        "user": user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at or int(datetime.utcnow().timestamp() + SESSION_TTL_SECONDS)
    }
    
    db_sess = DBSession(
        sid=sid,
        sess=session_data,
        expire=datetime.utcnow() + timedelta(seconds=SESSION_TTL_SECONDS)
    )
    db.add(db_sess)
    db.commit()
    return sid

def delete_session(db: Session, sid: str):
    row = db.query(DBSession).filter(DBSession.sid == sid).first()
    if row:
        db.delete(row)
        db.commit()

def upsert_user(db: Session, claims: dict) -> DBUser:
    user_id = claims.get("sub")
    if not user_id:
        raise ValueError("Claims must contain 'sub'")
        
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    
    first_name = claims.get("first_name") or claims.get("given_name")
    last_name = claims.get("last_name") or claims.get("family_name")
    profile_image_url = claims.get("profile_image_url") or claims.get("picture")
    
    if not user:
        user = DBUser(
            id=user_id,
            email=claims.get("email"),
            firstName=first_name,
            lastName=last_name,
            profileImageUrl=profile_image_url
        )
        db.add(user)
    else:
        user.email = claims.get("email") or user.email
        user.firstName = first_name or user.firstName
        user.lastName = last_name or user.lastName
        user.profileImageUrl = profile_image_url or user.profileImageUrl
        user.updatedAt = datetime.utcnow()
        
    db.commit()
    db.refresh(user)
    return user

def get_current_user():
    sid = get_session_id()
    if not sid:
        return None
    
    db = SessionLocal()
    try:
        session_data = get_session(db, sid)
        if session_data:
            return session_data.get("user")
    finally:
        db.close()
    return None

def is_replit_environment() -> bool:
    # Si REPL_ID está presente en el entorno, es el entorno real de Replit
    return bool(os.environ.get("REPL_ID"))
