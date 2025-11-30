import { useState } from "react";
import { predictImage } from "../api";

export default function UploadForm() {
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.elements.file.files[0];
    if (!file) return;

    const prediction = await predictImage(file);
    setResult(prediction);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" name="file" accept="image/*" />
        <button type="submit">Predict</button>
      </form>
      {result && (
        <div>
          <h3>Prediction: {result.class}</h3>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
