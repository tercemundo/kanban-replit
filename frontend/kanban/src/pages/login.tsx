import { useAuth } from "@workspace/auth-web";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const { login } = useAuth();

  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-4">
      <div className="max-w-md w-full border border-border bg-card p-8 rounded flex flex-col items-center">
        <h1 className="text-3xl font-bold text-primary mb-4 font-mono tracking-tighter">IT_KANBAN_OS</h1>
        <p className="text-muted-foreground text-center mb-8">System login required to access operational tasks.</p>
        <Button onClick={login} className="w-full font-bold">INITIATE LOGIN SEQUENCE</Button>
      </div>
    </div>
  );
}
