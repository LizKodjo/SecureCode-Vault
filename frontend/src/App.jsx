import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function App() {
  const [healthStatus, setHealthStatus] = useState("checking...");
  const [services, setServices] = useState({
    backend: "checking...",
    database: "checking...",
    redis: "checking...",
  });

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setHealthStatus("Healthy ✅");
      setServices((prev) => ({ ...prev, backend: "Connected ✅" }));
    } catch (error) {
      setHealthStatus("Unhealthy ❌");
      setServices((prev) => ({ ...prev, backend: "Disconnected ❌" }));
      console.error("Backend health check failed: ", error);
    }
  };

  return (
    <div>
      <div className="header">
        <div className="container">
          <h1>SecureCode Vault</h1>
          <p>A secure platform for code snippet management</p>
        </div>
      </div>

      <div className="container">
        <div className="card">
          <h2>Welcome to SecureCode Vault</h2>
          <p>
            This is the frontend for your SecureCode Vault application. The
            system is currently running in development mode.
          </p>

          <div className="status-grid">
            <div className="status-item">
              <h3>Backend API</h3>
              <p>{services.backend}</p>
            </div>
            <div className="status-item">
              <h3>Overall Status</h3>
              <p>{healthStatus}</p>
            </div>
            <div className="status-item">
              <h3>Frontend</h3>
              <p>Running ✅</p>
            </div>
          </div>

          <div className="api-links">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="api-link"
            >
              View API Documentation
            </a>
            <a
              href="http://localhost:8000/redoc"
              target="_blank"
              rel="noopener noreferrer"
              className="api-link"
            >
              View ReDoc
            </a>
          </div>
        </div>

        <div className="card">
          <h3>Next Steps</h3>
          <ul style={{ lineHeight: "1.6", marginLeft: "1.5rem" }}>
            <li>Backend API is running on port 8000</li>
            <li>Frontend is running on port 3000</li>
            <li>PostgreSQL database is running</li>
            <li>Redis is running for caching</li>
            <li>Check the API docs to test endpoints</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
