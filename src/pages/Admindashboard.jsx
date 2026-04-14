import { useState } from "react";
import {
  ShieldAlert,
  LayoutDashboard,
  ClipboardList,
  LogOut,
  Search,
  ChevronDown,
  Activity,
  CheckCircle2,
  Clock,
  Filter
} from "lucide-react";

const URGENCY_CONFIG = {
  Low: { color: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200", dot: "bg-emerald-500", bar: "bg-emerald-500" },
  Medium: { color: "text-amber-700", bg: "bg-amber-50 border-amber-200", dot: "bg-amber-500", bar: "bg-amber-500" },
  High: { color: "text-orange-700", bg: "bg-orange-50 border-orange-200", dot: "bg-orange-500", bar: "bg-orange-500" },
  Critical: { color: "text-red-700", bg: "bg-red-50 border-red-200", dot: "bg-red-500", bar: "bg-red-500" },
};

const STATUS_OPTIONS = ["Pending", "Under Review", "Resolved"];
const STATUS_CONFIG = {
  Pending: { color: "text-amber-700", bg: "bg-amber-50 border-amber-200" },
  "Under Review": { color: "text-blue-700", bg: "bg-blue-50 border-blue-200" },
  Resolved: { color: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200" },
};

export default function AdminDashboard({ incidents, onStatusUpdate, onLogout, session }) {
  const [search, setSearch] = useState("");
  const [filterUrgency, setFilterUrgency] = useState("All");
  const [filterStatus, setFilterStatus] = useState("All");
  const [selected, setSelected] = useState(null);
  const [activeSection, setActiveSection] = useState("incidents");

  const filtered = incidents.filter((inc) => {
    const matchSearch =
      inc.reporterName.toLowerCase().includes(search.toLowerCase()) ||
      inc.description.toLowerCase().includes(search.toLowerCase()) ||
      inc.reporterDesignation.toLowerCase().includes(search.toLowerCase());
    const matchUrgency = filterUrgency === "All" || inc.urgency === filterUrgency;
    const matchStatus = filterStatus === "All" || inc.status === filterStatus;
    return matchSearch && matchUrgency && matchStatus;
  });

  const stats = {
    total: incidents.length,
    pending: incidents.filter((i) => i.status === "Pending").length,
    reviewing: incidents.filter((i) => i.status === "Under Review").length,
    resolved: incidents.filter((i) => i.status === "Resolved").length,
    critical: incidents.filter((i) => i.urgency === "Critical").length,
  };

  return (
    <div className="h-screen bg-slate-50 text-slate-900 flex overflow-hidden relative">
      {/* Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-60 right-0 w-[500px] h-[500px] bg-blue-400/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-cyan-400/10 rounded-full blur-3xl" />
        <div className="absolute inset-0 opacity-[0.4]" style={{ backgroundImage: "linear-gradient(rgba(148, 163, 184, 0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(148, 163, 184, 0.2) 1px, transparent 1px)", backgroundSize: "60px 60px" }} />
      </div>

      {/* Sidebar */}
      <aside className="relative z-20 w-64 h-screen bg-white border-r border-slate-200 flex flex-col hidden md:flex shadow-sm shrink-0">
        <div className="p-6 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-md shadow-blue-500/20">
              <ShieldAlert className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="font-bold text-slate-900">IncidentIQ</div>
              <div className="text-slate-500 text-xs uppercase tracking-widest font-medium">Admin Panel</div>
            </div>
          </div>
        </div>

        <div className="p-4 flex-1 overflow-y-auto custom-scrollbar">
          <div className="text-slate-400 text-xs uppercase tracking-widest mb-3 px-2 font-semibold">Navigation</div>
          {[
            { key: "incidents", label: "Incidents", icon: ClipboardList, badge: stats.pending },
            { key: "overview", label: "Overview", icon: LayoutDashboard },
          ].map((item) => (
            <button
              key={item.key}
              onClick={() => setActiveSection(item.key)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all mb-1 hover:bg-slate-50 ${
                activeSection === item.key
                  ? "bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-50"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {item.label}
              {item.badge > 0 && (
                <span className="ml-auto bg-amber-100 text-amber-700 text-xs font-bold px-2 py-0.5 rounded-full border border-amber-200">
                  {item.badge}
                </span>
              )}
            </button>
          ))}
        </div>

        <div className="p-4 border-t border-slate-200 shrink-0">
          <div className="flex items-center gap-3 mb-3 px-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-xs font-bold text-white shadow-sm">
              {session?.displayName[0]}
            </div>
            <div>
              <div className="text-slate-900 text-sm font-medium">{session?.displayName}</div>
              <div className="text-slate-500 text-xs">Administrator</div>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-red-600 hover:text-red-700 hover:bg-red-50 text-sm font-medium transition-all"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 relative z-10 overflow-y-auto flex flex-col h-screen">
        {/* Mobile header - Fixed on mobile */}
        <div className="sticky top-0 z-30 md:hidden border-b border-slate-200 bg-white/80 backdrop-blur-md px-4 py-3 flex items-center justify-between shadow-sm shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
              <ShieldAlert className="w-4 h-4 text-white" />
            </div>
            <span className="text-slate-900 font-bold">IncidentIQ Admin</span>
          </div>
          <button onClick={onLogout} className="text-red-600 text-sm hover:text-red-700 font-medium">Logout</button>
        </div>

        <div className="p-6 max-w-5xl w-full">
          {/* Stats row */}
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
            {[
              { label: "Total", val: stats.total, text: "text-blue-600" },
              { label: "Pending", val: stats.pending, text: "text-amber-600" },
              { label: "Reviewing", val: stats.reviewing, text: "text-cyan-600" },
              { label: "Resolved", val: stats.resolved, text: "text-emerald-600" },
              { label: "Critical", val: stats.critical, text: "text-red-600" },
            ].map((s) => (
              <div key={s.label} className="bg-white border border-slate-200 shadow-sm rounded-2xl p-4">
                <div className={`text-3xl font-bold ${s.text}`}>{s.val}</div>
                <div className="text-slate-500 text-xs uppercase tracking-widest mt-1 font-semibold">{s.label}</div>
              </div>
            ))}
          </div>

          {activeSection === "incidents" && (
            <>
              <div className="flex flex-col sm:flex-row gap-3 mb-6 sticky top-0 md:relative z-20 pt-1 md:pt-0 pb-2 bg-slate-50/50 md:bg-transparent backdrop-blur-sm md:backdrop-blur-none">
                <div className="relative flex-1">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search incidents, reporters..."
                    className="w-full bg-white border border-slate-200 rounded-xl pl-11 pr-4 py-3 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm transition-all shadow-sm"
                  />
                </div>
                <div className="flex gap-2">
                  <div className="relative">
                    <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
                    <select
                      value={filterUrgency}
                      onChange={(e) => setFilterUrgency(e.target.value)}
                      className="bg-white border border-slate-200 rounded-xl pl-9 pr-4 py-3 text-slate-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm transition-all min-w-[140px] shadow-sm appearance-none"
                    >
                      <option value="All">All Urgency</option>
                      {["Low", "Medium", "High", "Critical"].map((u) => <option key={u}>{u}</option>)}
                    </select>
                  </div>
                  <div className="relative">
                    <Activity className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
                    <select
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                      className="bg-white border border-slate-200 rounded-xl pl-9 pr-4 py-3 text-slate-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm transition-all min-w-[140px] shadow-sm appearance-none"
                    >
                      <option value="All">All Status</option>
                      {STATUS_OPTIONS.map((s) => <option key={s}>{s}</option>)}
                    </select>
                  </div>
                </div>
              </div>

              <div className="space-y-3 pb-8">
                {filtered.length === 0 ? (
                  <div className="bg-white border border-slate-200 shadow-sm rounded-3xl p-12 text-center">
                    <div className="text-4xl mb-3">🔍</div>
                    <p className="text-slate-500 font-medium">No incidents match your filters.</p>
                  </div>
                ) : (
                  filtered.map((inc) => {
                    const urg = URGENCY_CONFIG[inc.urgency] || URGENCY_CONFIG.Medium;
                    const sts = STATUS_CONFIG[inc.status] || STATUS_CONFIG.Pending;
                    const isSelected = selected?.id === inc.id;
                    return (
                      <div
                        key={inc.id}
                        className="bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden hover:border-blue-300 hover:shadow-md transition-all duration-300"
                      >
                        <div
                          className="p-5 cursor-pointer"
                          onClick={() => setSelected(isSelected ? null : inc)}
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1 min-w-0">
                              <div className="flex flex-wrap items-center gap-2 mb-2">
                                <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${urg.bg} ${urg.color}`}>
                                  <span className={`w-1.5 h-1.5 rounded-full ${urg.dot} ${inc.urgency === "Critical" ? "animate-ping" : ""}`} />
                                  {inc.urgency}
                                </span>
                                <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-semibold border ${sts.bg} ${sts.color}`}>
                                  {inc.status}
                                </span>
                                <span className="text-slate-400 text-xs font-mono ml-1">#{String(inc.id).slice(-8)}</span>
                              </div>
                              <p className="text-slate-800 text-sm leading-relaxed line-clamp-2">{inc.description}</p>
                              <div className="flex flex-wrap gap-4 mt-2 text-xs text-slate-500">
                                <span>{inc.reporterName} · {inc.reporterDesignation}</span>
                                <span>{inc.date} {inc.time}</span>
                              </div>
                            </div>
                            <ChevronDown
                              className={`w-5 h-5 text-slate-400 shrink-0 transition-transform duration-200 ${isSelected ? "rotate-180" : ""}`}
                            />
                          </div>
                        </div>

                        {/* Expanded detail */}
                        {isSelected && (
                          <div className="border-t border-slate-200 bg-slate-50 p-5 space-y-4">
                            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                              {[
                                { label: "Reporter", val: inc.reporterName },
                                { label: "Designation", val: inc.reporterDesignation },
                                { label: "Date", val: inc.date },
                                { label: "Time", val: inc.time },
                              ].map((f) => (
                                <div key={f.label}>
                                  <div className="text-slate-500 text-xs uppercase tracking-widest mb-1 font-semibold">{f.label}</div>
                                  <div className="text-slate-900 text-sm font-bold">{f.val}</div>
                                </div>
                              ))}
                            </div>
                            <div>
                              <div className="text-slate-500 text-xs uppercase tracking-widest mb-2 font-semibold">Full Description</div>
                              <p className="text-slate-800 text-sm leading-relaxed bg-white rounded-xl p-4 border border-slate-200 shadow-sm">
                                {inc.description}
                              </p>
                            </div>
                            <div>
                              <div className="text-slate-500 text-xs uppercase tracking-widest mb-2 font-semibold">Update Status</div>
                              <div className="flex gap-2 flex-wrap">
                                {STATUS_OPTIONS.map((st) => {
                                  const cfg = STATUS_CONFIG[st];
                                  return (
                                    <button
                                      key={st}
                                      onClick={() => { onStatusUpdate(inc.id, st); setSelected({ ...inc, status: st }); }}
                                      className={`px-4 py-2 rounded-xl text-sm font-semibold border transition-all ${
                                        inc.status === st
                                          ? `${cfg.bg} ${cfg.color} scale-[1.03] shadow-sm`
                                          : "bg-white border-slate-200 text-slate-600 hover:border-slate-300 hover:text-slate-800 shadow-sm"
                                      }`}
                                    >
                                      {st}
                                    </button>
                                  );
                                })}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })
                 )}
              </div>
            </>
          )}

          {activeSection === "overview" && (
            <div className="space-y-6 pb-8">
              <h2 className="text-slate-900 font-bold text-xl">System Overview</h2>
              {/* Urgency breakdown */}
              <div className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6">
                <h3 className="text-slate-900 font-bold mb-5 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  Incidents by Urgency
                </h3>
                <div className="space-y-4">
                  {["Critical", "High", "Medium", "Low"].map((lvl) => {
                    const count = incidents.filter((i) => i.urgency === lvl).length;
                    const pct = incidents.length ? Math.round((count / incidents.length) * 100) : 0;
                    const cfg = URGENCY_CONFIG[lvl];
                    return (
                      <div key={lvl}>
                        <div className="flex justify-between text-sm mb-1.5">
                          <span className={`font-semibold ${cfg.color}`}>{lvl}</span>
                          <span className="text-slate-500 font-medium">{count} incidents ({pct}%)</span>
                        </div>
                        <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${cfg.bar} rounded-full transition-all duration-700`}
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Status breakdown */}
              <div className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6">
                <h3 className="text-slate-900 font-bold mb-5 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-500" />
                  Resolution Status
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {STATUS_OPTIONS.map((st) => {
                    const count = incidents.filter((i) => i.status === st).length;
                    const cfg = STATUS_CONFIG[st];
                    return (
                      <div key={st} className={`${cfg.bg} border rounded-xl p-4 text-center shadow-sm`}>
                        <div className={`text-3xl font-bold ${cfg.color}`}>{count}</div>
                        <div className="text-slate-600 text-xs mt-1 font-semibold uppercase">{st}</div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Recent activity */}
              <div className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6">
                <h3 className="text-slate-900 font-bold mb-5 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  Recent Activity
                </h3>
                <div className="space-y-3">
                  {incidents.slice(0, 5).map((inc) => {
                    const urg = URGENCY_CONFIG[inc.urgency];
                    return (
                      <div key={inc.id} className="flex items-center gap-3">
                        <span className={`w-2 h-2 rounded-full ${urg.dot} shrink-0`} />
                        <span className="text-slate-700 text-sm flex-1 truncate">{inc.description.slice(0, 80)}...</span>
                        <span className="text-slate-400 text-xs shrink-0 font-medium">{inc.date}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}