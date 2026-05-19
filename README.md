# IT Kanban Board OS (v4)

Plataforma de gestión de tareas y flujos de trabajo (Kanban) diseñada específicamente para la gerencia de sistemas y soporte tecnológico. Permite la visualización de estados, asignación departamental y priorización mediante una interfaz moderna con efectos de glassmorfismo y fondos dinámicos.

## 🏗️ Arquitectura y Stack Tecnológico

El proyecto está diseñado como un **Monorepositorio** que divide claramente el frontend, el backend y el contrato de la API.

### Frontend
- **Framework:** React 18 con Vite
- **Lenguaje:** TypeScript estricto
- **Estilos:** Tailwind CSS v4 + Vanilla CSS (Mesh Gradients)
- **Componentes UI:** Shadcn UI + Radix UI
- **Manejo de Estado/Data:** TanStack Query (React Query)
- **Drag & Drop:** `@hello-pangea/dnd`
- **Generación de Cliente:** Orval (genera los hooks de React Query a partir de OpenAPI)

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Servidor ASGI:** Uvicorn
- **ORM y Base de Datos:** SQLAlchemy + PostgreSQL 16
- **Validación de Datos:** Pydantic
- **Contrato de API:** OpenAPI 3.1.0 (`openapi.yaml`)

### Infraestructura
- **Proxy Inverso:** Nginx (Alpine)
- **Orquestación:** Docker Compose

---

## 🗺️ Diagrama de Arquitectura

```mermaid
graph TD
    Client[Navegador / Cliente Web] -->|HTTP/HTTPS| Nginx[Nginx Reverse Proxy\nPort 80]
    
    subgraph Frontend Container
        Nginx -->|/assets, /| Vite[Vite / React SPA\nPort 3000]
    end
    
    subgraph Backend Container
        Nginx -->|/api/*| FastAPI[FastAPI + Uvicorn\nPort 8080]
        FastAPI -.->|Lee Especificación| OpenAPI[openapi.yaml]
    end
    
    subgraph Database Container
        FastAPI -->|Lectura/Escritura| Postgres[(PostgreSQL 16\nPort 5432)]
    end
    
    subgraph Build Time
        OpenAPI -.->|Orval Genera| APIClient[Cliente React / Hooks]
        APIClient -.-> Vite
    end
```

---

## 🔌 Puertos de la Aplicación

Cuando se ejecuta mediante Docker Compose, los servicios exponen o utilizan internamente los siguientes puertos:

| Servicio | Puerto Host | Puerto Interno | Descripción |
|----------|-------------|----------------|-------------|
| **Nginx (Proxy)** | `80` | `80` | Entrada principal. Redirige a Frontend o Backend. |
| **Frontend** | N/A | `3000` | Expuesto solo a la red interna de Docker. |
| **Backend** | `8080` | `8080` | API expuesta para llamadas directas o swagger (`/docs`). |
| **PostgreSQL** | N/A | `5432` | Aislado en la red interna de Docker. |

> **Nota:** La documentación interactiva de la API está disponible en `http://localhost:8080/docs` una vez levantado el entorno.

---

## 🚀 Instalación y Despliegue

### Opción A: Con Docker (Recomendado)

La forma más rápida de levantar todo el ecosistema con cero configuración.

**Requisitos:** Docker y Docker Compose instalados.

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repo>
   cd kanban-replit
   ```
2. Levantar los contenedores en segundo plano:
   ```bash
   docker compose up --build -d
   ```
3. Acceder a la aplicación:
   - Web: [http://localhost](http://localhost)
   - Swagger API: [http://localhost:8080/docs](http://localhost:8080/docs)

*(Para limpiar la base de datos y reiniciar de cero, ejecutar: `docker compose down -v`)*

---

### Opción B: Sin Docker (Desarrollo Local Independiente)

Si necesitás trabajar en los servicios por separado o no tenés Docker.

**Requisitos:** Node.js (v20+), pnpm, Python 3.12+ y PostgreSQL corriendo localmente.

**1. Configurar y levantar la Base de Datos Local**
- Instalá Postgres y creá una base de datos.
- Seteá la variable de entorno en tu terminal:
  ```bash
  export DATABASE_URL="postgresql://usuario:password@localhost:5432/kanbandb"
  ```

**2. Levantar el Backend (FastAPI)**
```bash
cd backend/api
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

**3. Instalar Monorepo y Levantar Frontend**
En una nueva terminal, desde la raíz del proyecto:
```bash
# Instalar dependencias globales (workspace)
pnpm install

# Generar el cliente API desde openapi.yaml
pnpm --filter @workspace/api-client-react run generate

# Levantar frontend de desarrollo
pnpm --filter @workspace/kanban run dev
```

---

## 📋 Pendientes y Deuda Técnica (Roadmap)

La rama actual (`v4`) estableció una arquitectura limpia y una interfaz moderna. Sin embargo, para que el sistema esté "Production-Ready", faltan los siguientes hitos:

### 1. Login y Autenticación (OAuth / Sigo)
- Actualmente el sistema de Auth y el middleware de login están "mockeados" (simulados) a través de `use-auth.ts` y las rutas base de `/api/login`.
- **Tarea:** Unificar la autenticación con el proveedor de la empresa (Sigo) o implementar un flujo real OAuth 2.0 / OpenID Connect.
- **Tarea:** Remover los mocks (`mock-user-123`) e inyectar el usuario real en la base de datos `users`.

### 2. Revisión de Seguridad (SecOps)
- **CORS:** Actualmente configurado con `allow_origins=["*"]` en `app.py`. Debe restringirse únicamente a los dominios de la empresa.
- **Manejo de Secretos:** Implementar `.env` y sistemas de inyección de secretos (ej. AWS Secrets Manager o Doppler) para las credenciales de PostgreSQL. Actualmente usan los valores por defecto del compose.
- **Cookies:** Asegurar que los tokens de sesión se emitan como cookies `HttpOnly`, `Secure` y `SameSite=Strict`.

### 3. Funcionalidades del Kanban
- **Paginación:** Implementar paginación en el backend si el volumen de tarjetas `DONE` crece demasiado.
- **WebSockets / SSE:** Actualmente la interfaz usa Optimistic Updates o polling al mover tareas. Implementar WebSockets permitiría que múltiples usuarios vean cómo se mueven las tarjetas en tiempo real sin recargar.
- **Auditoría:** Crear una tabla de historial (`task_history`) para saber quién movió qué tarjeta y cuándo.
