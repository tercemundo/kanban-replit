import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, Depends
from models import User, Session as DBSession
from database import SessionLocal

# ==============================================================================
# Variables de Configuración y Entorno
# ==============================================================================

# Si existe REPL_ID, asumimos que estamos en Replit
is_replit_environment = "REPL_ID" in os.environ

# Identificador de la cookie de sesión (compartido con React)
SESSION_COOKIE = "kanban_session_id"
SESSION_TTL_DAYS = 30
SESSION_TTL_SECONDS = SESSION_TTL_DAYS * 24 * 60 * 60

# ==============================================================================
# Funciones Base de Base de Datos
# ==============================================================================

def upsert_user(db: Session, user_info: Dict[str, Any]) -> User:
    """Busca al usuario por su ID externo (sub) o lo crea/actualiza."""
    sub = user_info.get("sub")
    if not sub:
        raise ValueError("Missing 'sub' in user info")

    user = db.query(User).filter(User.externalId == sub).first()

    if user:
        user.email = user_info.get("email") or user.email
        user.firstName = user_info.get("first_name") or user.firstName
        user.lastName = user_info.get("last_name") or user.lastName
        user.profileImageUrl = user_info.get("profile_image_url") or user.profileImageUrl
        user.updatedAt = datetime.utcnow()
    else:
        user = User(
            externalId=sub,
            email=user_info.get("email"),
            firstName=user_info.get("first_name"),
            lastName=user_info.get("last_name"),
            profileImageUrl=user_info.get("profile_image_url")
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    return user

def create_session(db: Session, user_data: Dict[str, Any], access_token: str, refresh_token: str = None) -> str:
    """Crea una sesión segura en la DB y devuelve el session_id (uuid)"""
    sid = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(days=SESSION_TTL_DAYS)
    
    new_sess = DBSession(
        sid=sid,
        accessToken=access_token,
        refreshToken=refresh_token,
        expiresAt=expires,
        userData=user_data
    )
    db.add(new_sess)
    db.commit()
    return sid

def delete_session(db: Session, sid: str):
    """Elimina la sesión de la base de datos"""
    sess = db.query(DBSession).filter(DBSession.sid == sid).first()
    if sess:
        db.delete(sess)
        db.commit()

# ==============================================================================
# Inyección de Dependencias para FastAPI
# ==============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session_id(request: Request) -> Optional[str]:
    """Extrae el SID de la cabecera Authorization o de las cookies"""
    # 1. Probar Bearer Token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split("Bearer ")[1].strip()
    
    # 2. Probar Cookie
    return request.cookies.get(SESSION_COOKIE)

def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[Dict[str, Any]]:
    """Devuelve los datos del usuario si la sesión es válida y no ha expirado"""
    sid = get_session_id(request)
    if not sid:
        return None
        
    sess = db.query(DBSession).filter(DBSession.sid == sid).first()
    if not sess:
        return None
        
    if sess.expiresAt and sess.expiresAt < datetime.utcnow():
        delete_session(db, sid)
        return None
        
    # Verificar que el usuario asociado a esta sesión aún exista en la DB
    if not sess.userData or "id" not in sess.userData:
        return None
        
    user = db.query(User).filter(User.id == sess.userData["id"]).first()
    if not user:
        return None
        
    return user.to_dict()

def require_auth(request: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Dependency que obliga a estar autenticado. Lanza 401 si no hay sesión."""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
