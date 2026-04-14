import { useState } from "react";
import {
  ShieldAlert,
  User,
  ShieldCheck,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
  Loader2,
  ArrowRight
} from "lucide-react";

const USERS = {
  user: { password: "user123", role: "user", displayName: "Alex Morgan" },
  admin: { password: "admin123", role: "admin", displayName: "Admin Control" },
};

export default function Login({ onLogin }) {
  const [tab, setTab] = useState("user");
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = () => {
    setError("");
    setLoading(true);
    setTimeout(() => {
      const credentials = USERS[form.username];
      if (
        credentials &&
        credentials.password === form.password &&
        credentials.role === tab
      ) {
        onLogin({ username: form.username, role: tab, displayName: credentials.displayName });
      } else {
        setError("Invalid credentials. Please try again.");
      }
      setLoading(false);
    }, 900);
  };

  const fillDemo = () => {
    if (tab === "user") setForm({ username: "user", password: "user123" });
    else setForm({ username: "admin", password: "admin123" });
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-900/10 rounded-full blur-3xl" />
        {/* Grid lines */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(96,165,250,1) 1px, transparent 1px), linear-gradient(90deg, rgba(96,165,250,1) 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Logo */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg shadow-blue-500/30 mb-4">
            <ShieldAlert className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">IncidentIQ</h1>
          <p className="text-blue-300/70 text-sm mt-1 tracking-widest uppercase">Incident Management System</p>
        </div>

        {/* Card */}
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl shadow-black/40">
          {/* Role Tabs */}
          <div className="flex bg-white/5 rounded-2xl p-1 mb-8 gap-1">
            {["user", "admin"].map((role) => (
              <button
                key={role}
                onClick={() => { setTab(role); setForm({ username: "", password: "" }); setError(""); }}
                className={`flex-1 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center justify-center gap-2 ${
                  tab === role
                    ? "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg shadow-blue-500/30"
                    : "text-blue-200/60 hover:text-blue-200"
                }`}
              >
                {role === "user" ? (
                  <User className="w-4 h-4" />
                ) : (
                  <ShieldCheck className="w-4 h-4" />
                )}
                {role.charAt(0).toUpperCase() + role.slice(1)} Login
              </button>
            ))}
          </div>

          {/* Fields */}
          <div className="space-y-4">
            <div className="group">
              <label className="block text-xs font-semibold text-blue-300/70 uppercase tracking-widest mb-2">Username</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-blue-400/50">
                  <User className="w-4 h-4" />
                </span>
                <input
                  type="text"
                  value={form.username}
                  onChange={(e) => setForm({ ...form, username: e.target.value })}
                  onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                  placeholder={tab === "user" ? "user" : "admin"}
                  className="w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-blue-400/50 focus:bg-white/8 transition-all text-sm"
                />
              </div>
            </div>

            <div className="group">
              <label className="block text-xs font-semibold text-blue-300/70 uppercase tracking-widest mb-2">Password</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-blue-400/50">
                  <Lock className="w-4 h-4" />
                </span>
                <input
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                  placeholder="••••••••"
                  className="w-full bg-white/5 border border-white/10 rounded-xl pl-11 pr-12 py-3 text-white placeholder-white/20 focus:outline-none focus:border-blue-400/50 focus:bg-white/8 transition-all text-sm"
                />
                <button
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-blue-400/50 hover:text-blue-300 transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="mt-4 flex items-center gap-2 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 text-red-300 text-sm">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          {/* Submit */}
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full mt-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold text-sm shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 disabled:opacity-60 disabled:scale-100 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Authenticating...
              </>
            ) : (
              <>
                Sign In
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

          {/* Demo hint */}
          <button
            onClick={fillDemo}
            className="w-full mt-3 py-2.5 rounded-xl border border-white/10 text-blue-300/60 text-xs hover:text-blue-300/90 hover:border-white/20 transition-all"
          >
            Fill demo credentials →
          </button>
        </div>

        <p className="text-center text-blue-300/30 text-xs mt-6">
          IncidentIQ v2.0 · Secure Access Portal
        </p>
      </div>
    </div>
  );
}
