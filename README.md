# IT Kanban Board 📊🛡️

Una plataforma profesional y moderna de gestión de tareas tipo **Kanban** diseñada para empresas de tecnología/IT. Cuenta con arrastrar y soltar (drag-and-drop), filtrado avanzado por departamentos, estadísticas en tiempo real, validación estricta de formularios y seguridad mediante autenticación robusta.

Este proyecto está construido bajo una arquitectura de **Monorepositorio** moderna basada en **pnpm workspaces** y sigue un enfoque de desarrollo **Contract-First** (el contrato OpenAPI define toda la comunicación).

---

## 🛠️ Tecnologías Utilizadas (Tech Stack)

### **Frontend (Cliente)**
*   **React 19** + **Vite** — Interfaz ágil y moderna.
*   **Tailwind CSS v4** — Estilos ultrarrápidos y modulares.
*   **shadcn/ui** + **Lucide React** — Componentes de interfaz premium y accesibles.
*   **@hello-pangea/dnd** — Arrastrar y soltar fluido para las tareas del Kanban.
*   **Wouter** — Enrutamiento ligero y veloz para React.

### **Backend (API Server)**
*   **Node.js 24** + **TypeScript 5.9** — Entorno seguro y tipado.
*   **Express 5** — Servidor web robusto de última generación.
*   **Orval** — Generación de cliente API automática a partir de OpenAPI.
*   **Zod (v4)** + **Drizzle-Zod** — Validación estricta en el servidor y tipado unificado.

### **Base de Datos y Seguridad**
*   **PostgreSQL** — Motor de base de datos relacional robusto.
*   **Drizzle ORM** — ORM moderno de TypeScript para consultas ultrarrápidas y migraciones seguras.
*   **Replit Auth** (OpenID Connect / PKCE) — Inicio de sesión unificado y seguridad a nivel de sesión.

---

## 📁 Estructura del Proyecto (Monorepositorio)

El proyecto utiliza **pnpm workspaces** para separar las responsabilidades de forma limpia y reutilizable.

```text
it-kanban-board/
├── artifacts/                  # Aplicaciones Principales (Workspaces)
│   ├── kanban/                 # Frontend React de la aplicación
│   ├── api-server/             # Servidor backend Express 5
│   └── mockup-sandbox/         # Entorno de pruebas / Mockups de UI
├── lib/                        # Librerías Compartidas (Workspaces)
│   ├── api-spec/               # Contrato de API (OpenAPI yaml) y configuración de Orval
│   ├── api-client-react/       # Hooks de React Query auto-generados para el Frontend
│   ├── api-zod/                # Esquemas Zod auto-generados para validación del Servidor
│   ├── db/                     # Configuración de Drizzle ORM y esquemas de base de datos
│   └── replit-auth-web/        # Hook de autenticación personalizado (useAuth) para navegador
├── scripts/                    # Scripts de utilidad del monorepositorio
├── docker-compose.yml          # Orquestación de contenedores (API, DB, Nginx)
├── nginx.conf                  # Configuración de proxy inverso para producción local
├── pnpm-workspace.yaml         # Configuración de workspaces de pnpm
└── package.json                # Dependencias y scripts globales
```

---

## 🚀 Instalación y Uso Local

### **Requisitos Previos**
*   **Node.js v24** o superior.
*   **pnpm** (se recomienda usar pnpm para manejar los workspaces eficientemente).
*   Una base de datos **PostgreSQL** activa (puedes proveer tu cadena de conexión local).

### **Pasos para Iniciar**

1.  **Instalar dependencias globales y del monorepositorio:**
    ```bash
    pnpm install
    ```

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto basándote en el ejemplo proporcionado:
    ```bash
    cp .env.example .env
    ```
    Edita `.env` y agrega tu cadena de conexión a PostgreSQL en `DATABASE_URL`.

3.  **Preparar la Base de Datos (Drizzle ORM):**
    Aplica el esquema de la base de datos a tu PostgreSQL:
    ```bash
    pnpm --filter @workspace/db run push
    ```

4.  **Iniciar en Desarrollo:**
    Puedes levantar los servidores de desarrollo tanto de la API como del Frontend en paralelo:
    *   **Ejecutar Servidor API (Puerto 8080):**
        ```bash
        pnpm --filter @workspace/api-server run dev
        ```
    *   **Ejecutar Frontend (Puerto 18929):**
        ```bash
        pnpm --filter @workspace/kanban run dev
        ```

---

## 🖥️ Scripts Útiles Disponibles

Desde la raíz del proyecto puedes utilizar los siguientes comandos globales con `pnpm`:

*   `pnpm run typecheck` — Realiza una comprobación estricta de tipos de TypeScript en todo el monorepositorio.
*   `pnpm run build` — Compila y empaqueta todos los paquetes listos para producción.
*   `pnpm --filter @workspace/api-spec run codegen` — Regenera los hooks de React Query y los esquemas Zod a partir del archivo OpenAPI (`openapi.yaml`). Ejecútalo cada vez que hagas cambios en el contrato de la API.

---

## 📐 Decisiones de Arquitectura Clave

1.  **Contract-First (Contrato Primero):**
    El archivo `lib/api-spec/openapi.yaml` es la **fuente de la verdad**. Cualquier cambio en los endpoints, inputs o outputs se define allí primero. Luego, mediante `codegen`, se autogeneran los tipos de TypeScript y hooks de llamadas para el frontend, y los esquemas Zod de validación para el backend. **Nunca se escriben llamadas a la API o validadores a mano**.
2.  **Aislamiento de Tareas (Multi-tenant por Usuario):**
    Todas las tareas del Kanban están vinculadas a la sesión del usuario (`userId`). Ningún usuario puede ver, modificar o interactuar con las tareas de otros usuarios.
3.  **Actualización Optimista (Optimistic UI):**
    Al arrastrar y soltar una tarea entre columnas, el estado de la UI se actualiza inmediatamente de forma optimista mientras la petición viaja al backend, asegurando una experiencia de usuario sumamente fluida.
4.  **Autenticación Protegida:**
    Las rutas críticas del Kanban están protegidas en el cliente mediante el hook `@workspace/replit-auth-web` (`useAuth()`), redirigiendo inmediatamente a la página de login a los usuarios no autenticados.

---

## 📦 Características del Producto (Kanban Board)

*   **Pizarra Interactiva:** 4 estados de flujo de trabajo (Todo, En Progreso, En Revisión, Hecho).
*   **Tarjetas Detalladas:** Muestran título, descripción, prioridad (Alta, Media, Baja, con código de color dinámico), responsable asignado y fecha de vencimiento.
*   **Panel de Estadísticas en Tiempo Real:** Barra superior dinámica que muestra el recuento de tareas activas por columna.
*   **Filtro por Departamento:** Filtra instantáneamente la pizarra por departamentos IT (Técnicos IT, Gerencia Comercial, Gerencia Finanzas, Gerencia RRHH).
*   **Formularios con Validación Estricta:** Modales interactivos para crear y editar tareas garantizando la integridad de los datos.
*   **Diálogos de Confirmación:** Protección contra eliminaciones accidentales.

---

## ⚠️ Notas Importantes (Gotchas)
*   **Generación de código:** Si modificas `lib/api-spec/openapi.yaml`, debes correr la regeneración (`codegen`) para que las apps frontend y backend reflejen los nuevos cambios.
*   **Enrutamiento en Frontend:** No uses la función nativa `setLocation()` en renderizado con wouter, utiliza el componente `<Redirect to="..." />` para redirecciones limpias.
