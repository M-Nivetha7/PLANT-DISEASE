import { useState } from "react";
import API from "../api/api";

export default function Upload() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!image) {
      alert("Please select an image first");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("image", image);

      const response = await API.post("/predict", formData);
      setResult(response.data);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data) {
        alert(err.response.data.error || "Upload failed");
      } else {
        alert("Upload failed: " + err.message);
      }
    }
  };

  return (
    <div className="content">
      <h2>Upload Plant Leaf Image</h2>
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze</button>

      {result && (
        <div className="card">
          <h3>Disease: {result.disease}</h3>
          <p>Status: {result.status}</p>
          <p>Confidence: {result.confidence}%</p>
        </div>
      )}
    </div>
  );
}