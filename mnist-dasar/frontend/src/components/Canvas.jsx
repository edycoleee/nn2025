import { useRef, useState } from "react";
import { predictImage } from "../api";

export default function Canvas() {
  const canvasRef = useRef(null);
  const [result, setResult] = useState(null);

  const clearCanvas = () => {
    const ctx = canvasRef.current.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  };

  const handlePredict = async () => {
    const canvas = canvasRef.current;
    canvas.toBlob(async (blob) => {
      const file = new File([blob], "digit.png", { type: "image/png" });
      const prediction = await predictImage(file);
      setResult(prediction);
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
          };
        }}
      />
      <div style={{ marginTop: "10px" }}>
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={handlePredict}>Predict</button>
      </div>
      {result && (
        <div>
          <h3>Digit: {result.digit}</h3>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
