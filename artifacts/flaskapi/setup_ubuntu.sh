#!/usr/bin/env bash
# ==============================================================================
# Script de Configuración para Servidores Ubuntu
# ==============================================================================
set -e

echo "=== [1/5] Actualizando el sistema e instalando dependencias ==="
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm git libpq-dev build-essential

echo "=== [2/5] Instalando pnpm de forma global ==="
sudo npm install -g pnpm

echo "=== [3/5] Creando entorno virtual de Python (venv) ==="
python3 -m venv venv
source venv/bin/activate

echo "=== [4/5] Instalando requerimientos de Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [5/5] Instalando dependencias de Node.js en el Monorepositorio ==="
cd ../..
pnpm install

echo "=============================================================================="
echo " ¡Configuración completada con éxito!"
echo " Para iniciar la aplicación, ejecuta:"
echo "   cd artifacts/flaskapi"
echo "   bash startup.sh"
echo "=============================================================================="
