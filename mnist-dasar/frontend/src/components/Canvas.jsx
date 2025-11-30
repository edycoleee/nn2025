// 

import { useRef, useState } from "react";
import { predictImage } from "../api";

export default function Canvas() {
  const canvasRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const clearCanvas = () => {
    const ctx = canvasRef.current.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    setPreview(null);
    setResult(null);
  };

  const handlePreview = () => {
    const canvas = canvasRef.current;
    const dataURL = canvas.toDataURL("image/png");
    setPreview(dataURL);
  };

  const handlePredict = async () => {
    const canvas = canvasRef.current;
    setLoading(true);
    canvas.toBlob(async (blob) => {
      const file = new File([blob], "digit.png", { type: "image/png" });
      const prediction = await predictImage(file);
      setResult(prediction);
      setLoading(false);
    });
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={200}
        height={200}
        style={{ border: "1px solid black", background: "white" }}
        onMouseDown={(e) => {
          const ctx = canvasRef.current.getContext("2d");
          ctx.lineWidth = 15;
          ctx.lineCap = "round";
          ctx.strokeStyle = "black";
          ctx.beginPath();
          ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
          canvasRef.current.onmousemove = (ev) => {
            ctx.lineTo(ev.offsetX, ev.offsetY);
            ctx.stroke();
          };
          canvasRef.current.onmouseup = () => {
            canvasRef.current.onmousemove = null;
            handlePreview();
          };
        }}
      />
      <div style={{ marginTop: "10px" }}>
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={handlePredict}>Predict</button>
      </div>

      {preview && (
        <div style={{ marginTop: "10px" }}>
          <h3>Preview:</h3>
          <img src={preview} alt="Canvas preview" width={100} height={100} />
        </div>
      )}

      {loading && <p>⏳ Processing...</p>}

      {result && (
        <div>
          <h3>Digit: {result.digit}</h3>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>

          <h3>Probabilities:</h3>
          <ul>
            {result.probabilities.map((p, idx) => (
              <li key={idx}>
                {idx}: {(p * 100).toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
