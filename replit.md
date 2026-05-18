# IT Kanban Board

A professional task management Kanban board for IT companies, with drag-and-drop, department filtering, real-time stats, and authentication.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm --filter @workspace/kanban run dev` — run the frontend (port 18929)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Frontend: React 19, Vite, Tailwind CSS 4, shadcn/ui, @hello-pangea/dnd
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Auth: Replit Auth (OpenID Connect / PKCE)
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `lib/api-spec/openapi.yaml` — API contract (source of truth)
- `lib/api-client-react/src/generated/` — Generated React Query hooks
- `lib/api-zod/src/generated/` — Generated Zod schemas for server validation
- `lib/db/src/schema/tasks.ts` — Tasks table schema
- `lib/db/src/schema/auth.ts` — Sessions table (required by Replit Auth)
- `lib/replit-auth-web/` — Browser auth hook (`useAuth`)
- `artifacts/api-server/src/routes/tasks.ts` — Tasks CRUD routes
- `artifacts/api-server/src/routes/auth.ts` — Auth routes (login/callback/logout)
- `artifacts/kanban/src/pages/kanban.tsx` — Main Kanban board page
- `artifacts/kanban/src/pages/login.tsx` — Login page

## Architecture decisions

- Contract-first: OpenAPI spec gates codegen which gates the frontend — all types are generated, never hand-written.
- All tasks are scoped per userId from the session — no user can see another's tasks.
- Drag-and-drop uses optimistic invalidation: `useMoveTask` fires immediately on drop, then `getListTasksQueryKey` and `getGetTaskStatsQueryKey` are invalidated to sync state.
- `openid-client` is externalized in esbuild config (`build.mjs`) — do not try to bundle it.
- Auth state in the browser uses `@workspace/replit-auth-web`'s `useAuth()` hook — never the generated API client hooks.

## Product

- **Kanban board** with 4 columns: Todo, En Progreso, En Revisión, Hecho
- **Task cards** with title, description, priority (High/Medium/Low with color codes), assignee, due date
- **Drag-and-drop** between columns — persists immediately to the database
- **Real-time stats bar** showing per-column task counts
- **Department filter** — Técnicos IT, Gerencia Comercial, Gerencia Finanzas, Gerencia RRHH
- **Create/edit task modal** with form validation
- **Delete with confirmation dialog**
- **Auth gate** — unauthenticated users are redirected to login

## Gotchas

- After changing `openapi.yaml`, always run `pnpm --filter @workspace/api-spec run codegen` before using updated types.
- `openid-client` must stay in the `external` list in `artifacts/api-server/build.mjs`.
- Do not use `setLocation()` during render in wouter — use `<Redirect to="..." />` instead.
- Drizzle enum values for priority/assignee/columnStatus must match exactly what's in `lib/db/src/schema/tasks.ts`.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._
