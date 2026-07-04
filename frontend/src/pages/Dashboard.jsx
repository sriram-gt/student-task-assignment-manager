import { useState, useEffect } from "react";
import { getMe, getTasks, getDashboardStats, searchTasks } from "../services/api";
import Navbar from "../components/Navbar";
import TaskCard from "../components/TaskCard";
import TaskForm from "../components/TaskForm";
import SearchBar from "../components/SearchBar";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, overdue: 0 });
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchAll = async () => {
    try {
      const [userRes, statsRes] = await Promise.all([getMe(), getDashboardStats()]);
      setUser(userRes.data);
      setStats(statsRes.data);
      await fetchTasks();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTasks = async (activeFilter = filter) => {
    const params = {};
    if (activeFilter === "completed") params.status = "completed";
    if (activeFilter === "pending") params.status = "pending";
    if (activeFilter === "high") params.priority = "high";
    const res = await getTasks(params);
    setTasks(res.data);
  };

  const handleSearch = async (q) => {
    const res = await searchTasks(q);
    setTasks(res.data);
  };

  const handleClearSearch = () => fetchTasks();

  const handleFilter = (f) => {
    setFilter(f);
    fetchTasks(f);
  };

  useEffect(() => { fetchAll(); }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-gray-500 text-lg">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar userName={user?.name} />

      <div className="max-w-4xl mx-auto px-4 py-8">

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total", value: stats.total, color: "bg-blue-500" },
            { label: "Completed", value: stats.completed, color: "bg-green-500" },
            { label: "Pending", value: stats.pending, color: "bg-yellow-500" },
            { label: "Overdue", value: stats.overdue, color: "bg-red-500" },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl shadow p-4 text-center">
              <div className={`text-3xl font-bold text-white ${s.color} rounded-lg py-2 mb-2`}>
                {s.value}
              </div>
              <p className="text-sm text-gray-600 font-medium">{s.label}</p>
            </div>
          ))}
        </div>

        {/* Search */}
        <SearchBar onSearch={handleSearch} onClear={handleClearSearch} />

        {/* Filters + Add Button */}
        <div className="flex justify-between items-center mb-4 flex-wrap gap-2">
          <div className="flex gap-2 flex-wrap">
            {["", "pending", "completed", "high"].map((f) => (
              <button
                key={f}
                onClick={() => handleFilter(f)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition ${
                  filter === f
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-600 hover:bg-gray-200"
                }`}
              >
                {f === "" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>

          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-medium"
          >
            + New Task
          </button>
        </div>

        {/* Task List */}
        {tasks.length === 0 ? (
          <div className="text-center py-16 text-gray-400">
            <p className="text-5xl mb-4">📋</p>
            <p className="text-lg">No tasks yet. Create one!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onUpdate={fetchAll}
                onDelete={fetchAll}
              />
            ))}
          </div>
        )}
      </div>

      {showForm && (
        <TaskForm onClose={() => setShowForm(false)} onCreated={fetchAll} />
      )}
    </div>
  );
}