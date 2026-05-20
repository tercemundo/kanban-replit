import { useState, useEffect } from "react";
import { useAuth } from "@workspace/auth-web";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useListTasks, useGetTaskStats } from "@workspace/api-client-react";
import KanbanBoard from "@/components/kanban-board";
import TaskModal from "@/components/task-modal";
import HistoryModal from "@/components/history-modal";

export default function KanbanPage() {
  const { logout, user } = useAuth();
  const [assigneeFilter, setAssigneeFilter] = useState<string>("all");
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);

  const { data: tasks = [], isLoading } = useListTasks(
    assigneeFilter !== "all" ? { assignee: assigneeFilter } : {}
  );
  
  const { data: stats } = useGetTaskStats();

  return (
    <div className="min-h-screen bg-mesh-gradient text-foreground flex flex-col overflow-hidden">
      <header className="h-14 border-b border-border/50 px-6 flex items-center justify-between shrink-0 bg-card/60 backdrop-blur-xl z-10">
        <div className="flex items-center gap-6">
          <h1 className="font-bold text-primary text-xl font-mono tracking-tighter">IT_KANBAN_OS</h1>
          
          {stats && (
            <div className="flex gap-4 text-xs font-mono text-muted-foreground ml-4 hidden md:flex">
              <span className="font-semibold text-foreground">SYS_STATS:</span>
              <span>TOT:{stats.total}</span>
              <span className="text-secondary-foreground">TODO:{stats.todo}</span>
              <span className="text-chart-2">PROG:{stats.inProgress}</span>
              <span className="text-chart-3">REV:{stats.inReview}</span>
              <span className="text-chart-5">DONE:{stats.done}</span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-4">
          <Select value={assigneeFilter} onValueChange={setAssigneeFilter}>
            <SelectTrigger className="w-[180px] h-8 text-xs font-mono bg-background border-border">
              <SelectValue placeholder="FILTER_DEPT" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">MOSTRAR TODO</SelectItem>
              <SelectItem value="Técnicos IT">Técnicos IT</SelectItem>
              <SelectItem value="Gerencia Comercial">Gerencia Comercial</SelectItem>
              <SelectItem value="Gerencia Finanzas">Gerencia Finanzas</SelectItem>
              <SelectItem value="Gerencia RRHH">Gerencia RRHH</SelectItem>
            </SelectContent>
          </Select>

          <Button size="sm" onClick={() => setIsTaskModalOpen(true)} className="h-8 font-mono text-xs">
            + NEW_TASK
          </Button>

          <Button size="sm" variant="outline" onClick={() => setIsHistoryModalOpen(true)} className="h-8 font-mono text-xs border-primary/50 text-primary hover:bg-primary/10">
            TICKET_HISTORY
          </Button>

          <div className="h-4 w-[1px] bg-border mx-1"></div>

          <span className="text-xs font-mono text-muted-foreground hidden sm:inline-block">
            {user?.firstName?.toUpperCase()}
          </span>
          <Button variant="outline" size="sm" onClick={logout} className="h-8 font-mono text-xs">
            LOGOUT
          </Button>
        </div>
      </header>

      <main className="flex-1 overflow-x-auto overflow-y-hidden p-6">
        {isLoading ? (
          <div className="h-full flex items-center justify-center font-mono text-muted-foreground text-sm">
            LOADING_TASKS...
          </div>
        ) : (
          <KanbanBoard tasks={tasks} assigneeFilter={assigneeFilter} />
        )}
      </main>

      <TaskModal 
        open={isTaskModalOpen} 
        onOpenChange={setIsTaskModalOpen} 
      />
      <HistoryModal
        open={isHistoryModalOpen}
        onOpenChange={setIsHistoryModalOpen}
      />
    </div>
  );
}
