#!/usr/bin/env bash
# ==============================================================================
# Script de Configuración para Servidores Ubuntu (Sin Docker - SQLite)
# ==============================================================================
set -e

echo "=== [1/4] Instalando dependencias base ==="
sudo apt-get update -y
sudo apt-get install -y curl git libpq-dev build-essential python3 python3-pip python3-venv sqlite3 nodejs

echo "=== [2/4] Instalando pnpm de forma global ==="
if ! command -v pnpm &> /dev/null; then
    sudo npm install -g pnpm
fi

echo "=== [3/4] Creando entorno virtual de Python y sus dependencias ==="
cd backend/api
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ../..

echo "=== [4/4] Instalando dependencias del Frontend ==="
cd frontend
# Intentamos instalar. Si pnpm pide aprobación de builds, lo forzamos.
pnpm install || (echo "Reintentando con aprobación de builds..." && pnpm approve-builds && pnpm install)
cd ..

echo "=============================================================================="
echo " ¡Configuración completada con éxito (usando SQLite)!"
echo " Para iniciar la aplicación, ejecuta:"
echo "   bash startup.sh"
echo "=============================================================================="
