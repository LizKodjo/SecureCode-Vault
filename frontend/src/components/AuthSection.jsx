import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE;

export default function AuthSection({
  activeTab,
  setActiveTab,
  onLogin,
  onRegister,
}) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [snippets, setSnippets] = useState([]);
  const [loading, setLoading] = useState(false);

  //   Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchUserProfile(token);
    }
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    if (activeTab === "login") {
      onLogin(email, password);
    } else {
      onRegister(email, password);
    }
  }

  const fetchUserProfile = async (token) => {
    try {
      const response = await axios.get(`${API_BASE}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(response.data);
      setActiveTab("snippets");
      fetchSnippets(token);
    } catch (error) {
      console.error("Failed to fetch user profile: ", error);

      localStorage.removeItem("token");
    }
  };

  const fetchSnippets = async (token) => {
    try {
      const response = await axios.get(`${API_BASE}/snippets`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSnippets(response.data);
    } catch (error) {
      console.error("Failed to fetch snippets: ", error);
    }
  };

  return (
    <>
      <div className="auth-section">
        <div className="card">
          <div className="tabs">
            <button
              className={`tab ${activeTab === "login" ? "active" : ""}`}
              onClick={() => setActiveTab("login")}
            >
              Login
            </button>
            <button
              className={`tab ${activeTab === "register" ? "active" : ""}`}
              onClick={() => setActiveTab("register")}
            >
              Register
            </button>
          </div>
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Enter your email"
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Enter your password"
                minLength="6"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading
                ? "Processing..."
                : activeTab === "login"
                ? "Login"
                : "Register"}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
