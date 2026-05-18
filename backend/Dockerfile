FROM python:3.12-slim

WORKDIR /workspace

# Instalar dependencias necesarias para PostgreSQL y compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos de Python en cache
COPY backend/api/requirements.txt ./backend/api/
RUN pip install --no-cache-dir -r ./backend/api/requirements.txt

# Copiar código del backend y la especificación de la API (desde el contexto raíz)
COPY backend/ ./backend/
COPY shared/ ./shared/

WORKDIR /workspace/backend/api

EXPOSE 8080

# Iniciar el servidor FastAPI usando Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
