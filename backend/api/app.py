import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Importar los routers de la nueva arquitectura
from routers import root_router, api_router, auth_router

# Auto-crear las tablas de base de datos en caso de iniciar sin Alembic de inmediato
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="IT Kanban Board API",
    description="API para la gestión de tareas Kanban",
    version="3.0.0",
)

# Habilitar CORS para permitir peticiones del frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:18929", "http://127.0.0.1:18929", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar (montar) los enrutadores
app.include_router(root_router)
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(api_router, prefix="/api", tags=["Tasks"])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    # Uvicorn reemplaza a Gunicorn/Werkzeug en este nuevo entorno async
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
