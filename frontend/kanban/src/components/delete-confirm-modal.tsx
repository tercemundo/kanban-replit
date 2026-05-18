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
  taskId: number;
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
      <AlertDialogContent className="border-destructive/20">
        <AlertDialogHeader>
          <AlertDialogTitle className="font-mono text-destructive">DELETE_TASK?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the task from the system database.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={deleteTask.isPending}>CANCEL</AlertDialogCancel>
          <AlertDialogAction 
            onClick={(e) => { e.preventDefault(); handleConfirm(); }}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            disabled={deleteTask.isPending}
          >
            {deleteTask.isPending ? "DELETING..." : "CONFIRM_DELETE"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
