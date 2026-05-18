import { z } from "zod";

export const taskSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().optional().nullable(),
  priority: z.enum(["high", "medium", "low"]),
  assignee: z.enum(["Técnicos IT", "Gerencia Comercial", "Gerencia Finanzas", "Gerencia RRHH"]),
  columnStatus: z.enum(["todo", "in_progress", "in_review", "done"]),
  dueDate: z.string().optional().nullable(),
});

export type TaskFormData = z.infer<typeof taskSchema>;
