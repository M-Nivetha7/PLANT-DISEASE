import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import API from "../api/api";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function Analytics() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/analytics").then(res => setData(res.data));
  }, []);

  const chartData = {
    labels: data.map(d => d.disease),
    datasets: [
      {
        label: "Predictions",
        data: data.map(d => d.count),
        backgroundColor: "#22c55e"
      }
    ]
  };

  return (
    <div className="content">
      <h2>Disease Analytics</h2>
      <div className="card">
        <Bar data={chartData} />
      </div>
    </div>
  );
}