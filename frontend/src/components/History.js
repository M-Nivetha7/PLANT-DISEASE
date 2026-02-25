import { useEffect, useState } from "react";
import API from "../api/api";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    API.get("/analytics").then(res => setHistory(res.data));
  }, []);

  return (
    <div className="content">
      <h2>Prediction History</h2>
      {history.map((item, index) => (
        <div key={index} className="card">
          <h3>{item.disease}</h3>
          <p>Total Predictions: {item.count}</p>
        </div>
      ))}
    </div>
  );
}