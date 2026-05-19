FROM node:20-slim AS builder

WORKDIR /workspace

# Instalar pnpm de forma global
RUN npm install -g pnpm

# Copiar archivos de configuración del monorepositorio para el caché de pnpm
# Nota: desde v2, estos archivos viven en frontend/ (no en la raíz)
COPY frontend/package.json frontend/pnpm-workspace.yaml frontend/pnpm-lock.yaml ./frontend/
COPY frontend/tsconfig.json frontend/tsconfig.base.json ./frontend/

# Copiar las librerías propias del frontend
COPY frontend/lib/ ./frontend/lib/
COPY shared/ ./shared/

# Copiar la aplicación web principal
COPY frontend/kanban/ ./frontend/kanban/

# Instalar dependencias y compilar el bundle
RUN pnpm install --frozen-lockfile --dir ./frontend
RUN pnpm --filter @workspace/kanban run build

# Etapa 2: Servidor Nginx ligero para los estáticos
FROM nginx:alpine

# Copiar los archivos estáticos desde la etapa de compilación
COPY --from=builder /workspace/frontend/kanban/dist /usr/share/nginx/html

# Copiar la configuración del reverse proxy interna para React Router
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
