import { useNavigate } from "react-router-dom";

export default function Navbar({ userName }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow">
      <h1 className="text-xl font-bold tracking-wide">STAM</h1>
      <div className="flex items-center gap-4">
        <span className="text-sm">Welcome, {userName}</span>
        <button
          onClick={handleLogout}
          className="bg-white text-blue-600 text-sm px-3 py-1 rounded-lg hover:bg-gray-100 transition font-medium"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}