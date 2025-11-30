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

  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    const { data } = await axios.get('http://localhost:5000/students_with_images');
    setStudents(data);
  };

  const trainModel = async () => {
    const { data } = await axios.post('http://localhost:5000/train');
    alert(`Training selesai. Val Acc: ${(data.val_acc * 100).toFixed(1)}%`);
  };

  const [predictions, setPredictions] = useState([]);

  const predictImage = async (file) => {
    const form = new FormData();
    form.append('file', file);
    const { data } = await axios.post('http://localhost:5000/predict', form);
    setPredictions(data.top); // simpan semua hasil
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
        <hr />
        <input
          type="file"
          multiple
          onChange={e => setFiles([...e.target.files])}
        />
        <button onClick={uploadImages} disabled={!studentId}>Upload ≥5 Gambar</button>
        <hr />
        <button onClick={trainModel}>Train Model</button>
        <hr />
        <h3>Prediksi Gambar Baru</h3>
        <input type="file" onChange={e => predictImage(e.target.files[0])} />

        {predictions.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <h4>Hasil Prediksi:</h4>
            <ul>
              {predictions.map(p => (
                <li key={p.student_id}>
                  {p.name} — {(p.prob * 100).toFixed(2)}%
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div style={{ padding: 20 }}>
        <h2>Daftar Siswa + Gambar</h2>
        <button onClick={fetchStudents}>Load Data</button>
        <ul>
          {students.map(s => (
            <li key={s.id}>
              <strong>{s.name}</strong>
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                {s.images.map(img => (
                  <img
                    key={img.id}
                    src={`http://localhost:5000/${img.path}`}
                    alt={s.name}
                    width={100}
                  />
                ))}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
