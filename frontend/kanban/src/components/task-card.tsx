import { useState } from "react";
import { format } from "date-fns";
import { CalendarIcon, Edit2, Trash2 } from "lucide-react";
import { Task } from "@workspace/api-client-react/src/generated/api.schemas";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import TaskModal from "./task-modal";
import DeleteConfirmModal from "./delete-confirm-modal";

const PRIORITY_COLORS = {
  high: "#ef4444",
  medium: "#eab308",
  low: "#22c55e"
};

export default function TaskCard({ task }: { task: Task }) {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  return (
    <>
      <div className="group relative bg-background/80 backdrop-blur-sm border border-border/60 p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1 bg-background/90 backdrop-blur pb-1 pl-1 rounded-bl">
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setIsEditModalOpen(true)}>
            <Edit2 className="h-3 w-3" />
          </Button>
          <Button variant="ghost" size="icon" className="h-6 w-6 text-destructive hover:text-destructive" onClick={() => setIsDeleteModalOpen(true)}>
            <Trash2 className="h-3 w-3" />
          </Button>
        </div>

        <div className="flex gap-2 items-start mb-2 pr-12">
          <div 
            className="w-2 h-2 rounded-full mt-1.5 shrink-0" 
            style={{ backgroundColor: PRIORITY_COLORS[task.priority] }}
          />
          <h3 className="font-semibold text-sm leading-snug line-clamp-2">{task.title}</h3>
        </div>

        {task.description && (
          <p className="text-xs text-muted-foreground line-clamp-2 mb-3">
            {task.description}
          </p>
        )}

        <div className="mt-4 flex items-center justify-between">
          <Badge variant="secondary" className="text-[10px] px-1.5 py-0 font-mono font-medium rounded-sm border border-secondary-foreground/10 bg-secondary/50">
            {task.assignee}
          </Badge>

          {task.dueDate && (
            <div className="flex items-center text-[10px] font-mono text-muted-foreground">
              <CalendarIcon className="h-3 w-3 mr-1" />
              {format(new Date(task.dueDate), "MMM dd")}
            </div>
          )}
        </div>
      </div>

      <TaskModal 
        open={isEditModalOpen} 
        onOpenChange={setIsEditModalOpen} 
        task={task} 
      />
      
      <DeleteConfirmModal 
        open={isDeleteModalOpen} 
        onOpenChange={setIsDeleteModalOpen} 
        taskId={task.id} 
      />
    </>
  );
}
