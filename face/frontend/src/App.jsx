import { useEffect, useState } from "react";
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
      <h1>Face Recognition</h1>
      <p>Server status: {status}</p>
    </div>
  );
}

export default App;
