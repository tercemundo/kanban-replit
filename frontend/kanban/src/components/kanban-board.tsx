import { DragDropContext, Droppable, Draggable, DropResult } from "@hello-pangea/dnd";
import { useMoveTask, getListTasksQueryKey, getGetTaskStatsQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";
import { Task, TaskColumnStatus } from "@workspace/api-client-react/src/generated/api.schemas";
import TaskCard from "./task-card";

const COLUMNS: { id: TaskColumnStatus; title: string }[] = [
  { id: "todo", title: "TODO" },
  { id: "in_progress", title: "EN PROGRESO" },
  { id: "in_review", title: "EN REVISIÓN" },
  { id: "done", title: "HECHO" }
];

export default function KanbanBoard({ tasks }: { tasks: Task[] }) {
  const queryClient = useQueryClient();
  const moveTask = useMoveTask();

  const onDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const sourceColumn = result.source.droppableId as TaskColumnStatus;
    const destinationColumn = result.destination.droppableId as TaskColumnStatus;
    const taskId = parseInt(result.draggableId);

    if (sourceColumn === destinationColumn) return;

    // Optimistically update the UI if needed, or just let React Query handle it after mutation
    // For a simple case, we just trigger the mutation. The API is fast on localhost.
    
    moveTask.mutate(
      { id: taskId, data: { columnStatus: destinationColumn } },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: getListTasksQueryKey() });
          queryClient.invalidateQueries({ queryKey: getGetTaskStatsQueryKey() });
        }
      }
    );
  };

  return (
    <div className="h-full">
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="flex gap-6 h-full items-start">
          {COLUMNS.map(col => {
            const columnTasks = tasks.filter(t => t.columnStatus === col.id).sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
            
            return (
              <div key={col.id} className="flex-1 min-w-[300px] flex flex-col h-full bg-card rounded border border-border">
                <div className="p-3 border-b border-border bg-muted/30 flex items-center justify-between shrink-0">
                  <h2 className="font-mono text-sm font-bold text-foreground">{col.title}</h2>
                  <span className="text-xs font-mono bg-muted text-muted-foreground px-2 py-0.5 rounded">
                    {columnTasks.length}
                  </span>
                </div>
                
                <Droppable droppableId={col.id}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`flex-1 p-3 overflow-y-auto space-y-3 transition-colors ${
                        snapshot.isDraggingOver ? "bg-muted/10" : ""
                      }`}
                    >
                      {columnTasks.length === 0 && !snapshot.isDraggingOver && (
                        <div className="h-full flex items-center justify-center text-xs font-mono text-muted-foreground/50 border border-dashed border-border/50 rounded p-4 text-center">
                          NO_TASKS_IN_QUEUE
                        </div>
                      )}
                      
                      {columnTasks.map((task, index) => (
                        <Draggable key={task.id.toString()} draggableId={task.id.toString()} index={index}>
                          {(provided, snapshot) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className={snapshot.isDragging ? "opacity-90 scale-[1.02] shadow-xl" : ""}
                              style={provided.draggableProps.style}
                            >
                              <TaskCard task={task} />
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            );
          })}
        </div>
      </DragDropContext>
    </div>
  );
}
