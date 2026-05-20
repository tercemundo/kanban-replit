import { useState } from "react";
import { useAuth } from "@workspace/auth-web";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function LoginPage() {
  const { login, loginError } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const queryParams = new URLSearchParams(window.location.search);
  const isLoggedOut = queryParams.has("loggedOut");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await login(username, password);
    } catch (err) {
      // Error is handled in useAuth via loginError
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-mesh-gradient flex items-center justify-center p-4">
      <div className="max-w-md w-full border border-border/50 bg-card/80 backdrop-blur-2xl p-8 rounded-xl shadow-2xl flex flex-col items-center">
        <div className="w-16 h-1 w-primary bg-primary rounded-full mb-6"></div>
        <h1 className="text-3xl font-bold text-primary mb-2 font-mono tracking-tighter">IT_KANBAN_OS</h1>
        
        {isLoggedOut && !loginError && (
          <div className="mb-6 p-3 w-full bg-primary/10 border border-primary/20 rounded-md">
            <p className="text-primary text-[10px] font-mono text-center uppercase tracking-wider font-bold">
              gracias por usar nuestro sistemas.
            </p>
          </div>
        )}

        <p className="text-muted-foreground text-center mb-8 text-sm font-mono uppercase tracking-widest">Authentication Required</p>

        
        <form onSubmit={handleSubmit} className="w-full space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-[10px] font-mono text-muted-foreground uppercase">Username</Label>
            <Input 
              id="username"
              type="text"
              placeholder="ENTER_ID"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="bg-background/50 border-border/50 font-mono text-sm h-11"
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-[10px] font-mono text-muted-foreground uppercase">Password</Label>
            <Input 
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-background/50 border-border/50 font-mono text-sm h-11"
              required
            />
          </div>

          {loginError && (
            <Alert variant="destructive" className="bg-destructive/10 border-destructive/20 text-destructive h-10 py-2 flex items-center">
              <AlertDescription className="text-[10px] font-mono uppercase tracking-tight">
                {loginError}
              </AlertDescription>
            </Alert>
          )}

          <Button 
            type="submit" 
            className="w-full h-11 font-bold font-mono tracking-widest uppercase transition-all hover:scale-[1.02] active:scale-95"
            disabled={isSubmitting}
          >
            {isSubmitting ? "AUTHENTICATING..." : "INITIATE_SESSION"}
          </Button>
        </form>
        
        <div className="mt-8 text-[9px] text-muted-foreground font-mono uppercase tracking-widest opacity-50">
          Secure Core Gateway v0.1.0
        </div>
      </div>
    </div>
  );
}
