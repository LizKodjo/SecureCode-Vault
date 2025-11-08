import { useEffect, useState } from "react";
// import "./App.css";
import axios from "axios";
import AuthSection from "./components/AuthSection";
import SnippetSection from "./components/SnippetSection";

const API_BASE = import.meta.env.VITE_API_BASE;

console.log("API Base URL:", API_BASE); // Debug log

function App() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState("login");
  const [loading, setLoading] = useState(false);
  const [snippets, setSnippets] = useState([]);
  const [newSnippet, setNewSnippet] = useState({
    title: "",
    language: "python",
    code: "",
  });

  // Check API connectivity on component mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        const response = await axios.get(`${API_BASE}/health`);
        console.log("API Health Check:", response.data);
      } catch (error) {
        console.error("API is not reachable:", error);
        alert(
          "Cannot connect to the backend API. Make sure the backend is running on http://localhost:8000"
        );
      }
    };
    checkAPI();
  }, []);

  const handleRegister = async (email, password) => {
    setLoading(true);
    try {
      console.log("Attempting registration...", { email, API_BASE });

      await axios.post(`${API_BASE}/auth/register`, {
        email,
        password,
      });

      await handleLogin(email, password);
    } catch (error) {
      console.error("Registration error details:", error);
      const errorMessage = error.response?.data?.detaill || error.message;
      alert(`Registration failed: ${errorMessage}`);
    } finally {
      setLoading(false);
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

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setSnippets([]);
    setActiveTab("login");
  };

  const handleCreateSnippet = async () => {
    console.log("Current newSnippet state:", newSnippet); // Debug log

    // Check if fields are filled
    if (!newSnippet.title.trim() || !newSnippet.code.trim()) {
      console.log("Validation failed - title or code is empty");
      alert("Please fill in title and code");
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      console.log("Creating snippet with data:", newSnippet); // Debug log

      const response = await axios.post(`${API_BASE}/snippets`, newSnippet, {
        headers: { Authorization: `Bearer ${token}` },
      });

      console.log("Snippet created successfully:", response.data);

      // Reset form
      setNewSnippet({ title: "", language: "python", code: "" });

      // Refresh snippets list
      await fetchSnippets(token);

      alert("Snippet created successfully!");
    } catch (error) {
      console.error("Snippet creation error:", error);
      const errorMessage = error.response?.data?.detail || error.message;
      alert("Failed to create snippet: " + errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleShareSnippet = async (snippetId) => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `${API_BASE}/snippets/${snippetId}/share`,
        { expires_hours: 24 },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const shareUrl = `${window.location.origin}/shared/${response.data.token}`;
      navigator.clipboard.writeText(shareUrl);
      alert("Share link copied to clipboard!");
    } catch (error) {
      alert(
        "Failed to share snippet: " +
          (error.response?.data?.detail || error.message)
      );
    }
  };

  const handleLogin = async (email, password) => {
    setLoading(true);
    try {
      console.log("Attempting login...", { email, API_BASE });

      const response = await axios.post(`${API_BASE}/auth/login`, {
        email,
        password,
      });
      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      await fetchUserProfile(access_token);
    } catch (error) {
      console.error("Login error details:", error);
      const errorMessage = error.response?.data?.detail || error.message;

      alert(`Login failed: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };
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

  return (
    <>
      <div className="app">
        <header className="header">
          <div className="container">
            <h1>🔒 SecureCode Vault</h1>
            <p>Secure code snippet management</p>
            {user && (
              <div className="user-info">
                <span>Welcome, {user.email}</span>
                <button onClick={handleLogout} className="btn btn-outline">
                  Logout
                </button>
              </div>
            )}
          </div>
        </header>
        <div className="container">
          {!user ? (
            <AuthSection
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              onLogin={handleLogin}
              onRegister={handleRegister}
              loading={loading}
            />
          ) : (
            <SnippetSection
              snippets={snippets}
              newSnippet={newSnippet}
              setNewSnippet={setNewSnippet}
              onCreateSnippet={handleCreateSnippet}
              onShareSnippet={handleShareSnippet}
              loading={loading}
            />
          )}
        </div>
        <footer className="footer">
          <div className="container">
            <p>SecureCode Vault - Your secure code snippet manager</p>
          </div>
        </footer>
      </div>
    </>
  );
}

export default App;
