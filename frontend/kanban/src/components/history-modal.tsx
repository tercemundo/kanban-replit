import { useGetTaskHistory } from "@workspace/api-client-react";
import { format } from "date-fns";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

export default function HistoryModal({ 
  open, 
  onOpenChange 
}: { 
  open: boolean; 
  onOpenChange: (open: boolean) => void;
}) {
  const { data: tasks, isLoading } = useGetTaskHistory();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="font-mono text-xl tracking-tighter">TICKET_HISTORY</DialogTitle>
        </DialogHeader>
        
        <ScrollArea className="flex-1 pr-4">
          {isLoading ? (
            <div className="py-8 text-center text-muted-foreground animate-pulse font-mono">LOADING_HISTORY...</div>
          ) : tasks && tasks.length > 0 ? (
            <div className="space-y-3">
              {tasks.map((task) => (
                <div 
                  key={task.id} 
                  className="flex items-center justify-between p-3 rounded-lg border border-border/50 bg-secondary/20 hover:bg-secondary/30 transition-colors"
                >
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-primary text-xs font-bold">TKT:{task.ticketNumber}</span>
                      <span className="font-semibold text-sm line-clamp-1">{task.title}</span>
                    </div>
                    <div className="flex items-center gap-2 text-[10px] text-muted-foreground font-mono">
                      <span>{task.assignee}</span>
                      <span>•</span>
                      <span className="uppercase">{task.columnStatus}</span>
                      <span>•</span>
                      <span>{format(new Date(task.createdAt), "MMM dd, HH:mm")}</span>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-[9px] uppercase font-mono">
                    {task.priority}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-8 text-center text-muted-foreground font-mono">NO_TICKETS_FOUND</div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
