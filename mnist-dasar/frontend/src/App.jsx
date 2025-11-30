import { useEffect, useState } from "react";
import UploadForm from "./components/UploadForm";
import { testConnection } from "./api";

function App() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    async function checkServer() {
      const result = await testConnection();
      if (result.error) {
        setStatus("❌ Backend not reachable");
      } else {
        setStatus("✅ " + result.message);
      }
    }
    // console.log("USE EFFECT")
    checkServer();
  }, []);

  return (
    <div>
      <h1>CIFAR Image Prediction</h1>
      <p>Server status: {status}</p>
      <UploadForm />
    </div>
  );
}

export default App;
