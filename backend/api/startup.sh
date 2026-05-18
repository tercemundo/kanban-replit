#!/usr/bin/env bash
# ==============================================================================
# Script de Inicio Concurrente (Desarrollo)
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

# 1. Cargar variables de entorno del archivo .env
ENV_FILE="../../.env"
if [ -f "$ENV_FILE" ]; then
    echo "Cargando variables de entorno desde $ENV_FILE..."
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# 2. Activar venv si existe
if [ -d "venv" ]; then
    echo "Activando entorno virtual venv..."
    source venv/bin/activate
fi

# 3. Arrancar Flask Backend en Puerto 8080
echo "=== Iniciando Flask API Backend en puerto 8080 ==="
python app.py &
BACKEND_PID=$!
sleep 2

# 4. Arrancar React Frontend en Puerto 18929
echo "=== Iniciando React Frontend en puerto 18929 ==="
cd ../../frontend
pnpm --filter @workspace/kanban run dev --port 18929 --host &
FRONTEND_PID=$!

# Esperar a que los procesos de fondo terminen
wait
