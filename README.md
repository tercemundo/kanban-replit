# IT Kanban Board 📊🛡️

Una plataforma profesional y moderna de gestión de tareas tipo **Kanban** diseñada para empresas de tecnología/IT. Cuenta con arrastrar y soltar (drag-and-drop), filtrado avanzado por departamentos, estadísticas en tiempo real, validación estricta de formularios y arquitectura limpia separando el frontend del backend.

---

## 🏗️ Arquitectura del Proyecto (v3)

Este proyecto está dividido en tres carpetas principales para mantener una clara separación de responsabilidades:

- **`/frontend`**: Contiene la aplicación cliente en React y todo el ecosistema de Node.js (configuraciones de `pnpm`).
  - `/frontend/kanban`: El proyecto Vite de React principal.
  - `/frontend/lib`: Librerías compartidas del lado cliente (cliente de API autogenerado, validaciones Zod, sistema de autenticación).
- **`/backend`**: Contiene el servidor de la API y las reglas de negocio.
  - `/backend/api`: Servidor en **Python (FastAPI)** con enrutamiento moderno y validación vía Pydantic.
  - `/backend/lib/db`: Esquemas de base de datos Drizzle/SQLAlchemy.
- **`/shared`**: Código compartido real entre cliente y servidor.
  - `/shared/api-spec`: Contrato `openapi.yaml` que define estrictamente todos los endpoints.

## 🛠️ Stack Tecnológico

- **Frontend:** React 19, Vite, Tailwind CSS 4, Framer Motion, pnpm workspaces.
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Alembic, Pydantic.
- **Base de Datos:** PostgreSQL 16.
- **Infraestructura:** Docker, Nginx Proxy.

---

## 🚀 Guía de Ejecución Rápida

Tienes dos opciones para ejecutar el proyecto. **La opción recomendada para cualquier desarrollador es utilizar Docker**, ya que configura automáticamente la base de datos, el backend y el frontend sin ensuciar tu sistema.

### Opción 1: Ejecutar usando Docker (Recomendado) 🐳

1. Asegúrate de tener **Docker** y **Docker Compose** instalados en tu computadora.
2. Abre una terminal en la raíz del proyecto.
3. Ejecuta el siguiente comando para construir y levantar todos los contenedores:

   ```bash
   docker compose up --build -d
   ```

4. ¡Listo! Todo estará en línea en un par de minutos. Podrás acceder a los servicios en las siguientes direcciones:
   - **Tablero Kanban (Frontend):** [http://localhost](http://localhost) o [http://localhost:3000](http://localhost:3000)
   - **API (Backend):** [http://localhost:8080/api/](http://localhost:8080/api/)
   - *Para detener el sistema:* `docker compose down`

### Opción 2: Ejecutar de forma Nativa (Ubuntu) 🐧

Si no deseas utilizar Docker y usas **Ubuntu/Linux**, puedes configurar los servicios directamente en tu sistema usando los scripts automatizados que preparamos para ti.

**Paso 1: Instalar dependencias del sistema**
Este script actualizará tus repositorios de Ubuntu e instalará Node.js, npm, pnpm, Python3 y librerías C esenciales.

```bash
cd backend/api
bash setup_ubuntu.sh
```

**Paso 2: Configurar la Base de Datos (Opcional si usas SQLite en dev)**
Por defecto, el backend buscará una variable `DATABASE_URL`. Si existe un archivo `.env` en la raíz que apunte a un Postgres corriendo de forma local, se conectará a él. En su defecto, se creará un entorno SQLite localmente.

**Paso 3: Levantar Frontend y Backend simultáneamente**
Este script arranca el servidor FastAPI (Python) en segundo plano y luego levanta la interfaz Vite de React, uniéndolos para que trabajen en conjunto.

```bash
cd backend/api
bash startup.sh
```
*(Para detener todo, simplemente presiona `Ctrl + C` en esa misma terminal y el script apagará todos los procesos de forma limpia).*

---


