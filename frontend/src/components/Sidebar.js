import { Link } from "react-router-dom";
import "../styles.css";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2>🌱 PlantCare AI</h2>
      <Link to="/">Dashboard</Link>
      <Link to="/upload">Upload</Link>
      <Link to="/analytics">Analytics</Link>
      <Link to="/history">History</Link>
    </div>
  );
}