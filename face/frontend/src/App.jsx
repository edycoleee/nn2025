import { useEffect, useState } from "react";
import { testConnection } from "./api";
import axios from 'axios';

function App() {
  const [status, setStatus] = useState("Checking...");

  const [name, setName] = useState('');
  const [studentId, setStudentId] = useState(null);
  const [files, setFiles] = useState([]);

  const createStudent = async () => {
    const { data } = await axios.post('http://localhost:5000/students', { name });
    setStudentId(data.id);
    alert(`Siswa dibuat: ${data.name} (id=${data.id})`);
  };

  const uploadImages = async () => {
    const form = new FormData();
    for (const f of files) form.append('files', f);
    const { data } = await axios.post(`http://localhost:5000/upload/${studentId}`, form);
    alert(`Upload sukses: ${data.saved.length} gambar`);
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
      <h2>Upload Banyak Gambar Siswa</h2>
      <input 
        type="text" 
        placeholder="Nama siswa" 
        value={name} 
        onChange={e => setName(e.target.value)} 
      />
      <button onClick={createStudent}>Buat Siswa</button>
      <hr/>
      <input 
        type="file" 
        multiple 
        onChange={e => setFiles([...e.target.files])} 
      />
      <button onClick={uploadImages} disabled={!studentId}>Upload ≥5 Gambar</button>
    </div>
    </div>
  );
}

export default App;
