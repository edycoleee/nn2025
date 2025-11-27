// App.jsx
import { useRef, useState } from 'react'
import axios from 'axios'

function App() {
  const canvasRef = useRef(null)
  const [result, setResult] = useState("")

  const handlePredict = async () => {
    const canvas = canvasRef.current
    const image = canvas.toDataURL("image/png")

    const res = await axios.post("http://localhost:5000/predict", {
      image: image
    })

    setResult(res.data.prediction)
  }

  const clearCanvas = () => {
    const ctx = canvasRef.current.getContext("2d")
    ctx.fillStyle = "white"
    ctx.fillRect(0, 0, 280, 280)
  }

  return (
    <div>
      <h1>MNIST Digit Recognizer</h1>
      <canvas
        ref={canvasRef}
        width={280}
        height={280}
        style={{ border: "1px solid black", background: "white" }}
        onMouseDown={e => {
          const ctx = canvasRef.current.getContext("2d")
          ctx.lineWidth = 20
          ctx.lineCap = "round"
          ctx.strokeStyle = "black"
          ctx.beginPath()
          ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY)
          canvasRef.current.onmousemove = ev => {
            ctx.lineTo(ev.offsetX, ev.offsetY)
            ctx.stroke()
          }
        }}
        onMouseUp={() => {
          canvasRef.current.onmousemove = null
        }}
      />
      <br />
      <button onClick={handlePredict}>Predict</button>
      <button onClick={clearCanvas}>Clear</button>
      <h2>Prediction: {result}</h2>
    </div>
  )
}

export default App
