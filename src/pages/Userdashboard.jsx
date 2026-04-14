import { useState } from "react";
import { DatePicker, TimePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import {
  ShieldAlert,
  LogOut,
  ListTodo,
  Hourglass,
  Search,
  CheckCircle,
  Plus,
  History,
  CheckCircle2,
  FileText,
  Send,
  User
} from "lucide-react";

const URGENCY_CONFIG = {
  Low: { color: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200", dot: "bg-emerald-500" },
  Medium: { color: "text-amber-700", bg: "bg-amber-50 border-amber-200", dot: "bg-amber-500" },
  High: { color: "text-orange-700", bg: "bg-orange-50 border-orange-200", dot: "bg-orange-500" },
  Critical: { color: "text-red-700", bg: "bg-red-50 border-red-200", dot: "bg-red-500" },
};

const STATUS_CONFIG = {
  Pending: { color: "text-amber-700", bg: "bg-amber-50 border-amber-200" },
  "Under Review": { color: "text-blue-700", bg: "bg-blue-50 border-blue-200" },
  Resolved: { color: "text-emerald-700", bg: "bg-emerald-50 border-emerald-200" },
};

export default function UserDashboard({ incidents, onAddIncident, onLogout, session }) {
  const [view, setView] = useState("form");
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({
    date: dayjs(),
    time: dayjs(),
    reporterName: "",
    reporterDesignation: "",
    description: "",
    urgency: "Medium",
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const e = {};
    if (!form.reporterName.trim()) e.reporterName = "Reporter name is required";
    if (!form.reporterDesignation.trim()) e.reporterDesignation = "Designation is required";
    if (!form.description.trim() || form.description.trim().length < 20)
      e.description = "Please provide at least 20 characters";
    return e;
  };

  const handleSubmit = () => {
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    
    // Format date and time for submission
    const formattedForm = {
      ...form,
      date: form.date.format('YYYY-MM-DD'),
      time: form.time.format('HH:mm'),
    };
    
    onAddIncident(formattedForm);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setForm({
        date: dayjs(),
        time: dayjs(),
        reporterName: "",
        reporterDesignation: "",
        description: "",
        urgency: "Medium",
      });
      setView("history");
    }, 2000);
  };

  const set = (key, val) => {
    setForm((f) => ({ ...f, [key]: val }));
    setErrors((e) => ({ ...e, [key]: undefined }));
  };

  return (
    <div className="h-screen bg-slate-50 relative text-slate-900 flex flex-col overflow-hidden">
      {/* Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-60 -right-60 w-[500px] h-[500px] bg-blue-400/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-60 -left-60 w-[500px] h-[500px] bg-cyan-400/10 rounded-full blur-3xl" />
        <div className="absolute inset-0 opacity-[0.4]" style={{ backgroundImage: "linear-gradient(rgba(148, 163, 184, 0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(148, 163, 184, 0.2) 1px, transparent 1px)", backgroundSize: "60px 60px" }} />
      </div>

      {/* Navbar */}
      <nav className="shrink-0 relative z-50 border-b border-slate-200 bg-white/70 backdrop-blur-xl">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-md shadow-blue-500/20">
              <ShieldAlert className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-slate-900">IncidentIQ</span>
              <span className="hidden sm:inline-block ml-2 text-xs text-slate-500 uppercase tracking-widest">User Portal</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 bg-blue-50 border border-blue-100 rounded-full px-3 py-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-blue-700 text-sm font-medium">{session?.displayName}</span>
            </div>
            <button onClick={onLogout} className="flex items-center gap-2 text-slate-500 hover:text-red-500 text-sm transition-colors font-medium">
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="flex-1 overflow-y-auto relative z-10 custom-scrollbar">
        <div className="max-w-5xl mx-auto px-6 py-8">
          {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total Filed", val: incidents.length, icon: <ListTodo /> },
            { label: "Pending", val: incidents.filter(i => i.status === "Pending").length, icon: <Hourglass /> },
            { label: "Under Review", val: incidents.filter(i => i.status === "Under Review").length, icon: <Search /> },
            { label: "Resolved", val: incidents.filter(i => i.status === "Resolved").length, icon: <CheckCircle /> },
          ].map((s) => (
            <div key={s.label} className="bg-white border border-slate-200 shadow-sm rounded-2xl p-4">
              <div className="text-2xl mb-1 text-blue-500">{s.icon}</div>
              <div className="text-2xl font-bold text-slate-900">{s.val}</div>
              <div className="text-xs text-slate-500 font-medium uppercase tracking-widest mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Tab Nav */}
        <div className="flex gap-2 mb-6 bg-slate-200/50 rounded-2xl p-1.5 border border-slate-200 w-fit">
          {[
            { key: "form", label: "New Report", icon: <Plus /> },
            { key: "history", label: `History (${incidents.length})`, icon: <History /> },
          ].map((t) => (
            <button
              key={t.key}
              onClick={() => setView(t.key)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 ${
                view === t.key
                  ? "bg-white text-slate-900 shadow-sm border border-slate-200"
                  : "text-slate-500 hover:text-slate-700 hover:bg-white/50"
              }`}
            >
              <span className="text-lg leading-none flex items-center">{t.icon}</span>
              {t.label}
            </button>
          ))}
        </div>

        {/* Form View */}
        {view === "form" && (
          <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm">
            {submitted ? (
              <div className="flex flex-col items-center justify-center py-16 gap-4">
                <div className="w-20 h-20 rounded-full bg-emerald-50 border-2 border-emerald-200 flex items-center justify-center animate-bounce">
                  <CheckCircle2 className="w-10 h-10 text-emerald-500" />
                </div>
                <h3 className="text-xl font-bold text-slate-900">Incident Reported!</h3>
                <p className="text-slate-500 text-sm text-center">Your report has been submitted successfully and is under review.</p>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-3 mb-8">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center">
                    <FileText className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h2 className="font-bold text-xl" style={{ color: '#000' }}>New Incident Report</h2>
                    <p className="text-slate-500 text-xs">Fill in the details below to submit a report</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  {/* Date */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-2">
                      Incident Date <span className="text-red-500">*</span>
                    </label>
                    <DatePicker
                      value={form.date}
                      onChange={(val) => set("date", val)}
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          size: "small",
                          sx: {
                            '& .MuiOutlinedInput-root': {
                              backgroundColor: '#f8fafc',
                              borderRadius: '0.75rem',
                              '& fieldset': { borderColor: '#e2e8f0' },
                              '&:hover fieldset': { borderColor: '#cbd5e1' },
                              '&.Mui-focused fieldset': { borderColor: '#3b82f6' },
                            },
                            '& .MuiInputBase-input': { padding: '6px 10px', fontSize: '0.6rem' },
                            '& .MuiInputAdornment-root .MuiSvgIcon-root': { fontSize: '0.85rem' }
                          }
                        }
                      }}
                    />
                  </div>

                  {/* Time */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-2">
                      Incident Time <span className="text-red-500">*</span>
                    </label>
                    <TimePicker
                      value={form.time}
                      onChange={(val) => set("time", val)}
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          size: "small",
                          sx: {
                            '& .MuiOutlinedInput-root': {
                              backgroundColor: '#f8fafc',
                              borderRadius: '0.75rem',
                              '& fieldset': { borderColor: '#e2e8f0' },
                              '&:hover fieldset': { borderColor: '#cbd5e1' },
                              '&.Mui-focused fieldset': { borderColor: '#3b82f6' },
                            },
                            '& .MuiInputBase-input': { padding: '6px 10px', fontSize: '0.6rem' },
                            '& .MuiInputAdornment-root .MuiSvgIcon-root': { fontSize: '0.85rem' }
                          }
                        }
                      }}
                    />
                  </div>

                  {/* Reporter Name */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-2">
                      Reporter Name <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={form.reporterName}
                      onChange={(e) => set("reporterName", e.target.value)}
                      placeholder="Your full name"
                      className={`w-full bg-slate-50 border rounded-xl px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none transition-all text-xs ${errors.reporterName ? "border-red-400 focus:border-red-500" : "border-slate-200 focus:border-blue-500"}`}
                    />
                    {errors.reporterName && <p className="text-red-500 text-[10px] mt-1">{errors.reporterName}</p>}
                  </div>

                  {/* Designation */}
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-2">
                      Reporter Designation <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={form.reporterDesignation}
                      onChange={(e) => set("reporterDesignation", e.target.value)}
                      placeholder="Your job title / role"
                      className={`w-full bg-slate-50 border rounded-xl px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none transition-all text-xs ${errors.reporterDesignation ? "border-red-400 focus:border-red-500" : "border-slate-200 focus:border-blue-500"}`}
                    />
                    {errors.reporterDesignation && <p className="text-red-500 text-[10px] mt-1">{errors.reporterDesignation}</p>}
                  </div>

                  {/* Urgency */}
                  <div className="sm:col-span-2">
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-3">
                      Urgency Level <span className="text-red-500">*</span>
                    </label>
                    <div className="grid grid-cols-4 gap-3">
                      {Object.entries(URGENCY_CONFIG).map(([level, cfg]) => (
                        <button
                          key={level}
                          onClick={() => set("urgency", level)}
                          className={`py-2 px-3 rounded-xl border text-xs font-semibold transition-all duration-200 ${
                            form.urgency === level
                              ? `${cfg.bg} ${cfg.color} scale-[1.02] shadow-sm`
                              : "bg-white border-slate-200 text-slate-500 hover:border-slate-300"
                          }`}
                        >
                          <div className={`w-1.5 h-1.5 rounded-full ${cfg.dot} mx-auto mb-1 ${form.urgency === level ? "animate-pulse" : "opacity-40"}`} />
                          {level}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Description */}
                  <div className="sm:col-span-2">
                    <label className="block text-xs font-semibold text-slate-600 uppercase tracking-widest mb-2">
                      Incident Description <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={form.description}
                      onChange={(e) => set("description", e.target.value)}
                      rows={4}
                      placeholder="Provide a detailed description of the incident — what happened, where, and any immediate actions taken..."
                      className={`w-full bg-slate-50 border rounded-xl px-4 py-3 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none transition-all text-xs resize-none ${errors.description ? "border-red-400 focus:border-red-500" : "border-slate-200 focus:border-blue-500"}`}
                    />
                    <div className="flex justify-between mt-1">
                      {errors.description ? <p className="text-red-500 text-[10px]">{errors.description}</p> : <span />}
                      <span className={`text-[10px] ${form.description.length < 20 ? "text-slate-400" : "text-emerald-500"}`}>
                        {form.description.length} / 20 min
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-3 mt-8">
                  <button
                    onClick={() => { setForm({ date: dayjs(), time: dayjs(), reporterName: "", reporterDesignation: "", description: "", urgency: "Medium" }); setErrors({}); }}
                    className="px-6 py-2.5 rounded-xl border border-slate-200 text-slate-500 hover:text-slate-700 hover:border-slate-300 hover:bg-slate-50 text-xs font-medium transition-all"
                  >
                    Reset
                  </button>
                  <button
                    onClick={handleSubmit}
                    className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold text-xs shadow-md shadow-blue-500/20 hover:shadow-lg hover:shadow-blue-500/30 hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2"
                  >
                    <Send className="w-3.5 h-3.5" />
                    Submit Incident Report
                  </button>
                </div>
              </>
            )}
          </div>
        )}

        {/* History View */}
        {view === "history" && (
          <div className="space-y-4">
            {incidents.length === 0 ? (
              <div className="bg-white border border-slate-200 shadow-sm rounded-3xl p-16 text-center">
                <div className="text-5xl mb-4">📭</div>
                <h3 className="text-slate-900 font-semibold text-lg">No incidents filed yet</h3>
                <p className="text-slate-500 text-sm mt-2">Your submitted reports will appear here.</p>
              </div>
            ) : (
              incidents.map((inc) => {
                const urg = URGENCY_CONFIG[inc.urgency];
                const sts = STATUS_CONFIG[inc.status] || STATUS_CONFIG.Pending;
                return (
                  <div
                    key={inc.id}
                    className="bg-white border border-slate-200 shadow-sm rounded-2xl p-6 hover:shadow-md hover:border-blue-200 transition-all duration-300 group"
                  >
                    <div className="flex flex-wrap items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-2 flex-wrap">
                          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${urg.bg} ${urg.color}`}>
                            <span className={`w-1.5 h-1.5 rounded-full ${urg.dot} animate-pulse`} />
                            {inc.urgency}
                          </span>
                          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${sts.bg} ${sts.color}`}>
                            {inc.status}
                          </span>
                          <span className="text-slate-400 text-xs font-mono">#{String(inc.id).slice(-6)}</span>
                        </div>
                        <p className="text-slate-700 text-sm leading-relaxed line-clamp-2">{inc.description}</p>
                        <div className="flex items-center gap-4 mt-3 text-xs text-slate-500 flex-wrap">
                          <span className="flex items-center gap-1">
                            <User className="w-3.5 h-3.5" />
                            {inc.reporterName} · {inc.reporterDesignation}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" />
                            {inc.date} at {inc.time}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}
      </div>
    </div>
  </div>
);
}
