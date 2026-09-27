import React, { useEffect, useState } from "react";
import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { api, clearToken, getToken, setToken } from "./services/api";

function Protected({ children }) {
  return getToken() ? children : <Navigate to="/login" replace />;
}

function Layout({ children }) {
  const navigate = useNavigate();
  return (
    <div className="app-shell">
      <nav className="navbar">
        <Link className="brand" to="/">DietCloud AI</Link>
        {getToken() && (
          <div className="nav-links">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/plans">Plans</Link>
            <Link to="/files">Files</Link>
            <button onClick={() => { clearToken(); navigate("/login"); }}>Logout</button>
          </div>
        )}
      </nav>
      <main className="container">{children}</main>
      <footer>Educational wellness demo • Synthetic data only • Not medical advice</footer>
    </div>
  );
}

function Home() {
  return (
    <section className="hero">
      <div>
        <span className="badge">Cloud Computing Project</span>
        <h1>AI-Powered Personal Diet Planner</h1>
        <p>
          Generate educational meal-plan examples, save them to a database,
          manage user files, and demonstrate authentication and cloud-ready architecture.
        </p>
        <div className="actions">
          <Link className="button" to="/register">Create Demo Account</Link>
          <Link className="button secondary" to="/login">Login</Link>
        </div>
      </div>
      <div className="hero-card">
        <h3>Cloud Concepts Demonstrated</h3>
        <ul>
          <li>REST API</li>
          <li>Authentication & authorization</li>
          <li>Database persistence</li>
          <li>Object storage</li>
          <li>AI fallback architecture</li>
          <li>Deployment readiness</li>
        </ul>
      </div>
    </section>
  );
}

function AuthForm({ mode }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      const result = mode === "register"
        ? await api.register(form)
        : await api.login({ email: form.email, password: form.password });
      setToken(result.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card auth-card">
      <h2>{mode === "register" ? "Create account" : "Welcome back"}</h2>
      {mode === "register" && (
        <label>Name<input value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></label>
      )}
      <label>Email<input type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} /></label>
      <label>Password<input type="password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} /></label>
      {error && <div className="error">{error}</div>}
      <button className="button" onClick={submit}>{mode === "register" ? "Register" : "Login"}</button>
    </div>
  );
}

function Profile() {
  const [profile, setProfile] = useState({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => { api.getProfile().then(setProfile).catch(e => setError(e.message)); }, []);

  function update(field, value) { setProfile(p => ({...p, [field]: value})); }

  async function save(e) {
    e.preventDefault();
    setMessage(""); setError("");
    try {
      await api.updateProfile({
        name: profile.name,
        age: profile.age ? Number(profile.age) : null,
        height: profile.height ? Number(profile.height) : null,
        weight: profile.weight ? Number(profile.weight) : null,
        activity_level: profile.activity_level || null,
        dietary_preference: profile.dietary_preference || null,
        goal: profile.goal || null,
        allergies: profile.allergies || "",
      });
      setMessage("Profile saved.");
    } catch (e) { setError(e.message); }
  }

  return (
    <div className="card">
      <h2>Demo Profile</h2>
      <p className="muted">Use synthetic information for this project.</p>
      <form onSubmit={save} className="form-grid">
        <label>Name<input value={profile.name || ""} onChange={e => update("name", e.target.value)} /></label>
        <label>Age<input type="number" value={profile.age || ""} onChange={e => update("age", e.target.value)} /></label>
        <label>Height (cm)<input type="number" value={profile.height || ""} onChange={e => update("height", e.target.value)} /></label>
        <label>Weight (kg)<input type="number" value={profile.weight || ""} onChange={e => update("weight", e.target.value)} /></label>
        <label>Activity level
          <select value={profile.activity_level || ""} onChange={e => update("activity_level", e.target.value)}>
            <option value="">Select</option><option value="low">Low</option><option value="moderate">Moderate</option><option value="high">High</option>
          </select>
        </label>
        <label>Diet preference
          <select value={profile.dietary_preference || ""} onChange={e => update("dietary_preference", e.target.value)}>
            <option value="">Select</option><option value="vegetarian">Vegetarian</option><option value="vegan">Vegan</option><option value="general">General / Non-Vegetarian</option>
          </select>
        </label>
        <label>Goal
          <select value={profile.goal || ""} onChange={e => update("goal", e.target.value)}>
            <option value="">Select</option><option value="balanced">General balanced eating</option><option value="weight-management">Weight-management demo</option><option value="fitness">Fitness-oriented demo</option>
          </select>
        </label>
        <label>Allergies/preferences (demo)<input value={profile.allergies || ""} onChange={e => update("allergies", e.target.value)} /></label>
        <div><button className="button">Save Profile</button></div>
      </form>
      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

function PlanCard({ plan, onDelete }) {
  return (
    <div className="plan-card">
      <div className="plan-header"><h3>Plan #{plan.id}</h3><small>{new Date(plan.created_at).toLocaleString()}</small></div>
      <div className="meal-grid">
        <div><b>Breakfast</b><p>{plan.breakfast}</p></div>
        <div><b>Lunch</b><p>{plan.lunch}</p></div>
        <div><b>Snack</b><p>{plan.snack}</p></div>
        <div><b>Dinner</b><p>{plan.dinner}</p></div>
      </div>
      <p><b>Nutrition summary:</b> {plan.nutrition_summary}</p>
      <p><b>Hydration:</b> {plan.hydration_reminder}</p>
      <button className="danger-button" onClick={() => onDelete(plan.id)}>Delete</button>
    </div>
  );
}

function Plans() {
  const [plans, setPlans] = useState([]);
  const [error, setError] = useState("");
  async function load() { try { setPlans(await api.getPlans()); } catch(e) { setError(e.message); } }
  useEffect(() => { load(); }, []);
  async function generate() {
    try { await api.generatePlan(); await load(); } catch(e) { setError(e.message); }
  }
  async function del(id) { await api.deletePlan(id); await load(); }

  return (
    <div>
      <div className="page-heading"><div><h2>Diet Plans</h2><p className="muted">Educational meal-plan examples.</p></div><button className="button" onClick={generate}>Generate New Plan</button></div>
      {error && <div className="error">{error}</div>}
      {plans.length === 0 ? <div className="empty">No saved plans yet. Complete your profile and generate one.</div> :
        plans.map(p => <PlanCard key={p.id} plan={p} onDelete={del} />)}
    </div>
  );
}

function Files() {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  async function load() { try { setFiles(await api.getFiles()); } catch(e) { setError(e.message); } }
  useEffect(() => { load(); }, []);

  async function upload(e) {
    const file = e.target.files[0];
    if (!file) return;
    try { await api.uploadFile(file); setMessage("File uploaded."); await load(); }
    catch(e) { setError(e.message); }
  }

  async function remove(id) { await api.deleteFile(id); await load(); }

  return (
    <div>
      <div className="card">
        <h2>Cloud Files</h2>
        <p className="muted">Local mode simulates object storage. The backend can be adapted to Supabase Storage.</p>
        <input type="file" accept=".jpg,.jpeg,.png,.webp,.pdf,.txt" onChange={upload} />
        {message && <div className="success">{message}</div>}
        {error && <div className="error">{error}</div>}
      </div>
      {files.map(file => (
        <div className="file-row" key={file.id}>
          <div><b>{file.filename}</b><span>{Math.round(file.size_bytes / 1024)} KB</span></div>
          <div className="actions">
            <button className="button small" onClick={async () => {
              const token = localStorage.getItem("token");
              const response = await fetch(api.downloadUrl(file.id), {
                headers: { Authorization: `Bearer ${token}` }
              });
              if (!response.ok) throw new Error("Download failed");
              const blob = await response.blob();
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = file.filename;
              a.click();
              URL.revokeObjectURL(url);
            }}>Download</button>
            <button className="danger-button" onClick={() => remove(file.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [plans, setPlans] = useState([]);
  useEffect(() => {
    Promise.all([api.getProfile(), api.getPlans()]).then(([p, plans]) => { setProfile(p); setPlans(plans); });
  }, []);
  if (!profile) return <div className="loading">Loading dashboard...</div>;
  return (
    <div>
      <div className="page-heading">
        <div><span className="badge">Protected Dashboard</span><h2>Welcome, {profile.name}</h2><p className="muted">Your cloud-ready personal workspace.</p></div>
        <Link className="button" to="/plans">Generate Plan</Link>
      </div>
      <div className="stats">
        <div className="stat"><span>Goal</span><b>{profile.goal || "Not set"}</b></div>
        <div className="stat"><span>Diet</span><b>{profile.dietary_preference || "Not set"}</b></div>
        <div className="stat"><span>Saved plans</span><b>{plans.length}</b></div>
      </div>
      {plans[0] && <PlanCard plan={plans[0]} onDelete={() => {}} />}
      {!plans[0] && <div className="empty">Complete your profile, then generate your first plan.</div>}
    </div>
  );
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<AuthForm mode="register" />} />
        <Route path="/login" element={<AuthForm mode="login" />} />
        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="/profile" element={<Protected><Profile /></Protected>} />
        <Route path="/plans" element={<Protected><Plans /></Protected>} />
        <Route path="/files" element={<Protected><Files /></Protected>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
