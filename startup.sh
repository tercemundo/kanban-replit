#!/usr/bin/env bash
# ==============================================================================
# Script de Inicio Concurrente (Sin Docker - SQLite)
# ==============================================================================

# Detener los procesos en segundo plano al salir (Ctrl + C)
cleanup() {
    echo ""
    echo "=== Apagando servicios ==="
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "Servicios detenidos."
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Cargar variables de entorno si existen
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo "Cargando variables de entorno desde $ENV_FILE..."
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Configuración obligatoria para SQLite local
export DATABASE_URL="sqlite:///./kanban.db"
export PORT="8080"

# 2. Arrancar FastAPI Backend
echo "=== Iniciando FastAPI Backend (SQLite) en puerto 8080 ==="
cd backend/api
if [ -d "venv" ]; then
    source venv/bin/activate
fi
uvicorn app:app --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!
cd ../..
sleep 2

# 3. Arrancar React Frontend
echo "=== Iniciando React Frontend en puerto 3000 ==="
cd frontend
pnpm --filter @workspace/kanban run dev --port 3000 --host &
FRONTEND_PID=$!
cd ..

# Esperar a que los procesos de fondo terminen
wait
