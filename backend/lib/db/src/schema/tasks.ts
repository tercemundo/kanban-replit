import { pgTable, text, serial, timestamp, pgEnum } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const priorityEnum = pgEnum("priority", ["high", "medium", "low"]);
export const assigneeEnum = pgEnum("assignee", [
  "Técnicos IT",
  "Gerencia Comercial",
  "Gerencia Finanzas",
  "Gerencia RRHH",
]);
export const columnStatusEnum = pgEnum("column_status", [
  "todo",
  "in_progress",
  "in_review",
  "done",
]);

export const tasksTable = pgTable("tasks", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  description: text("description"),
  priority: priorityEnum("priority").notNull().default("medium"),
  assignee: assigneeEnum("assignee").notNull(),
  columnStatus: columnStatusEnum("column_status").notNull().default("todo"),
  dueDate: timestamp("due_date", { withTimezone: true }),
  userId: text("user_id").notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true })
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date()),
});

export const insertTaskSchema = createInsertSchema(tasksTable).omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});
export type InsertTask = z.infer<typeof insertTaskSchema>;
export type Task = typeof tasksTable.$inferSelect;
