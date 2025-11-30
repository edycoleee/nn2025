import { useEffect, useState } from "react";
import { testConnection } from "./api";
import axios from 'axios';

function App() {
  const [status, setStatus] = useState("Checking...");

  const [name, setName] = useState('');
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const form = new FormData();
    form.append('name', name);
    form.append('file', file);
    const { data } = await axios.post('http://localhost:5000/upload', form);
    alert(`Siswa tersimpan: ${data.name}, id=${data.id}`);
  };

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
          <div style={{ padding: 20 }}>
      <h2>Upload Data Siswa</h2>
      <input 
        type="text" 
        placeholder="Nama siswa" 
        value={name} 
        onChange={e => setName(e.target.value)} 
      />
      <br/><br/>
      <input 
        type="file" 
        onChange={e => setFile(e.target.files[0])} 
      />
      <br/><br/>
      <button onClick={handleUpload}>Upload</button>
    </div>
    </div>
  );
}

export default App;
