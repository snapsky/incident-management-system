import { useState } from "react";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Login from "./pages/Login.jsx";
import UserDashboard from "./pages/Userdashboard.jsx";
import AdminDashboard from "./pages/Admindashboard.jsx";

export default function App() {
  const [session, setSession] = useState(null);
  const [incidents, setIncidents] = useState([
    {
      id: 1,
      reporterName: "Sarah Johnson",
      reporterDesignation: "Floor Supervisor",
      date: "2025-04-08",
      time: "09:15",
      description: "Electrical short circuit detected in server room B. Sparks observed near Panel 3. Area has been cordoned off pending inspection.",
      urgency: "Critical",
      status: "Under Review",
      submittedAt: "2025-04-08T09:20:00",
      username: "user",
    },
    {
      id: 2,
      reporterName: "Marcus Lee",
      reporterDesignation: "Security Officer",
      date: "2025-04-09",
      time: "14:30",
      description: "Unauthorized access attempt logged at Gate C. Badge scan failed 3 consecutive times. CCTV footage captured and forwarded.",
      urgency: "High",
      status: "Resolved",
      submittedAt: "2025-04-09T14:35:00",
      username: "user",
    },
    {
      id: 3,
      reporterName: "Priya Nair",
      reporterDesignation: "Warehouse Manager",
      date: "2025-04-10",
      time: "11:00",
      description: "Minor chemical spill in storage aisle 7. Estimated 2 litres of cleaning solvent. Spill contained with absorbent material.",
      urgency: "Medium",
      status: "Pending",
      submittedAt: "2025-04-10T11:05:00",
      username: "user",
    },
  ]);

  const addIncident = (incident) => {
    const newIncident = {
      ...incident,
      id: Date.now(),
      status: "Pending",
      submittedAt: new Date().toISOString(),
      username: session?.username,
    };
    setIncidents((prev) => [newIncident, ...prev]);
  };

  const updateIncidentStatus = (id, status) => {
    setIncidents((prev) =>
      prev.map((inc) => (inc.id === id ? { ...inc, status } : inc))
    );
  };

  const handleLogout = () => setSession(null);

  const renderContent = () => {
    if (!session) return <Login onLogin={setSession} />;
    if (session?.role === "admin")
      return (
        <AdminDashboard
          incidents={incidents}
          onStatusUpdate={updateIncidentStatus}
          onLogout={handleLogout}
          session={session}
        />
      );
    return (
      <UserDashboard
        incidents={incidents.filter((i) => i.username === session?.username)}
        onAddIncident={addIncident}
        onLogout={handleLogout}
        session={session}
      />
    );
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      {renderContent()}
    </LocalizationProvider>
  );
}
