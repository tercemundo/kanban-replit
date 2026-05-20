import { useDeleteTask, getListTasksQueryKey, getGetTaskStatsQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

export default function DeleteConfirmModal({ 
  open, 
  onOpenChange, 
  taskId 
}: { 
  open: boolean; 
  onOpenChange: (open: boolean) => void; 
  taskId: string;
}) {
  const queryClient = useQueryClient();
  const deleteTask = useDeleteTask();

  const handleConfirm = () => {
    deleteTask.mutate(
      { id: taskId },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: getListTasksQueryKey() });
          queryClient.invalidateQueries({ queryKey: getGetTaskStatsQueryKey() });
          onOpenChange(false);
        }
      }
    );
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent className="border-warning/20">
        <AlertDialogHeader>
          <AlertDialogTitle className="font-mono text-warning">MOVE_TO_DROP?</AlertDialogTitle>
          <AlertDialogDescription>
            This will move the task to the DROP column instead of deleting it. You can still recover it later if needed.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={deleteTask.isPending}>CANCEL</AlertDialogCancel>
          <AlertDialogAction 
            onClick={(e) => { e.preventDefault(); handleConfirm(); }}
            className="bg-warning text-warning-foreground hover:bg-warning/90"
            disabled={deleteTask.isPending}
          >
            {deleteTask.isPending ? "MOVING..." : "CONFIRM_DROP"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
