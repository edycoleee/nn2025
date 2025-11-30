
### SERVER UBUNTU
```txt

```
### GITHUB

```txt
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/nn2025.git
git push -u origin main
```

### REQUIREMENT
```py
# 1. Membuat Virtual Environtment
python3 -m venv venv
source venv/bin/activate  #Linux / Macbook
venv\Scripts\activate # Windows

#2. Install library
pip install matplotlib numpy
pip install seaborn
pip install scikit-learn
pip install tensorflow
pip install flask
```

# RAPBERYY PI 5

```py
sudo apt update
sudo apt upgrade -y

sudo apt install -y build-essential libssl-dev zlib1g-dev \
libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
tk-dev libffi-dev wget

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
sudo tar xzf Python-3.10.14.tgz
cd Python-3.10.14
sudo ./configure --enable-optimizations
sudo make -j4
sudo make altinstall

python3.10 --version

python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip

pip install tensorflow==2.13.0


python3 -c "import tensorflow as tf; print(tf.__version__)"
```

# GPU RTX 2060 Anda di laptop Asus ROG

install python versi 3.10

```
Cara Menginstal cuDNN (Zip Method)
Asumsi: Anda telah menginstal CUDA Toolkit 11.2 di lokasi default Windows, yaitu:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\
Langkah 1: Ekstrak File ZIP cuDNN
Temukan file ZIP cuDNN yang baru saja Anda unduh (misalnya, cudnn-windows-x86_64-8.1.0.27_cuda11.2-archive.zip).
Klik kanan pada file ZIP tersebut, lalu pilih Extract All... atau gunakan software seperti 7-Zip/WinRAR untuk mengekstrak isinya.
Setelah diekstrak, Anda akan mendapatkan sebuah folder baru dengan nama yang sama, dan di dalamnya terdapat tiga sub-folder utama:
- bin
- include
- lib
Langkah 2: Salin File ke Direktori CUDA
Sekarang, Anda perlu menyalin konten dari folder yang diekstrak tadi ke folder instalasi CUDA Anda.
Buka folder hasil ekstraksi cuDNN tadi.
Buka jendela File Explorer baru, dan navigasikan ke lokasi instalasi CUDA:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\
Salin konten:
Buka folder bin di folder cuDNN yang diekstrak. Salin semua file DLL di dalamnya.
Rekatkan (Paste) file-file tersebut ke dalam folder bin di direktori CUDA (C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin).
Lakukan hal yang sama untuk folder include dan lib.
Singkatnya, Anda memastikan bahwa file-file berikut berada di tempat yang benar:
File cuDNN	Lokasi Tujuan
...ekstrak...\bin\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
...ekstrak...\include\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include
...ekstrak...\lib\*.*	C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\lib
```
```cmd
py -3.10 --version

py -3.10 -m venv tf_gpu_env

.\tf_gpu_env\Scripts\activate
python --version 

python.exe -m pip install --upgrade pip
pip install tensorflow==2.10.0
pip install "numpy<2"
```
```
1. Verifikasi Ulang Pengaturan Path
Tekan tombol Windows + S, ketik "environment variables", dan buka "Edit the system environment variables".
Klik Environment Variables....
Di bagian System variables (bukan User variables), cari dan pilih Path, lalu klik Edit....
Pastikan dua jalur (path) berikut persis ada di daftar tersebut:

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\libnvvp

Restart Komputer Anda
```

```py
import tensorflow as tf
print(tf.__version__)
print(tf.test.is_gpu_available())


import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

```

```py
import tensorflow as tf

# Pastikan TensorFlow menggunakan GPU secara default
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please check your GPU setup, the default device is not set.")

# Contoh sederhana operasi di GPU
with tf.device('/GPU:0'):
    a = tf.constant([1.0, 2.0, 3.0], shape=[3], name='a')
    b = tf.constant([4.0, 5.0, 6.0], shape=[3], name='b')
    c = a + b

print(c)
```

### CIFAR

### MNIST

CNN MNIST + Flask API + React Vite dengan Canvas. Jadi user bisa menggambar angka di canvas frontend, kirim ke backend Flask, lalu CNN model prediksi angka (0–9)

```
mnist-project/
│
├── backend/
│   ├── app.py                # Flask API
│   ├── model/
│   │   └── mnist_cnn.h5      # Model CNN tersimpan
│   ├── utils/
│   │   └── preprocess.py     # Preprocessing gambar canvas
│   ├── requirements.txt
│   └── uploads/              # (opsional) simpan gambar
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
│           └── Canvas.jsx    # Komponen untuk menggambar angka
│
└── README.md
```

- Alur 1

User menggambar angka di canvas.

Canvas diubah jadi PNG blob → dikirim ke Flask API.

Flask preprocess → CNN prediksi angka.

Frontend tampilkan hasil prediksi + confidence.

- Alur 2

Backend kirim semua probabilitas kelas digit.

Frontend tampilkan list prosentase atau bar chart.

User bisa lihat distribusi prediksi, bukan hanya hasil tertinggi.

# FACE

## Tahap 1: Upload data. Jadi hanya backend untuk upload 1 gambar + simpan identitas siswa, dan frontend sederhana untuk form upload.

🛠 Backend Flask (Upload 1 gambar + identitas siswa)
Setup Flask + SQLite

Buat tabel students dengan kolom id, name, image_path.

Endpoint /upload menerima name + file gambar, lalu simpan ke folder data/raw.

pip install flask-cors


```python
# app.py
import os, sqlite3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/raw'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# init table
with get_db() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image_path TEXT NOT NULL
    )''')
    db.commit()

@app.post('/upload')
def upload_student():
    name = request.form.get('name')
    file = request.files.get('file')
    if not name or not file:
        return jsonify({'error':'name and file required'}), 400
    
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO students(name, image_path) VALUES (?,?)', (name, path))
    db.commit()
    sid = cur.lastrowid

    return jsonify({'id': sid, 'name': name, 'image_path': path})
```
👉 Jalankan dengan flask run (port default 5000).

🎨 Frontend React (Vite)
Setup project

```bash
npm create vite@latest frontend
cd frontend
npm install axios
```
Form upload sederhana

```jsx
// src/App.jsx
import { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [name, setName] = useState('');
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const form = new FormData();
    form.append('name', name);
    form.append('file', file);
    const { data } = await axios.post('http://localhost:5000/upload', form);
    alert(`Siswa tersimpan: ${data.name}, id=${data.id}`);
  };

  return (
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
  );
}
```
Proxy ke Flask (agar tidak kena CORS saat dev)

```js
// vite.config.js
export default {
  server: {
    proxy: {
      '/upload': 'http://localhost:5000'
    }
  }
}
```
🔄 Alur kerja
User isi nama + pilih 1 file gambar di frontend.

Klik Upload → request POST ke Flask /upload.

Flask simpan file ke data/raw/ dan metadata ke SQLite.

Response JSON berisi id, name, image_path.
=======================================
📌 Apa itu from werkzeug.utils import secure_filename
Werkzeug adalah library Python yang menjadi “toolkit” untuk web development, dan dipakai oleh Flask di belakang layar.

Di dalam werkzeug.utils ada fungsi bernama secure_filename.

Fungsi ini dipakai untuk membersihkan nama file upload agar aman disimpan di server.

🔒 Kenapa perlu secure_filename?
Saat user mengupload file, nama file bisa berisi:

Spasi, karakter aneh (?, *, .., /)

Path traversal (../../etc/passwd) → berbahaya!

Unicode atau simbol yang tidak cocok untuk sistem file

Jika langsung disimpan, bisa menimbulkan bug atau celah keamanan.

⚙️ Cara kerja secure_filename
Fungsi ini:

Menghapus karakter berbahaya.

Mengganti spasi dengan underscore _.

Menjaga hanya huruf, angka, titik, dan garis bawah.

Menghindari path traversal.

Contoh:

```python
from werkzeug.utils import secure_filename

filename = "my photo../evil.png"
safe = secure_filename(filename)
print(safe)   # hasil: "my_photo..evil.png"
```
👉 Jadi nama file yang tadinya berbahaya jadi aman untuk disimpan.


## Tahap 2: Upload banyak gambar per siswa (≥5). Tujuannya: setiap siswa bisa punya banyak gambar wajah (minimal 5) yang disimpan di backend, lalu frontend menyediakan form upload multi-file.

🛠 Backend Flask
Skema database
Kita pisahkan tabel students dan images:

```sql
CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  path TEXT NOT NULL,
  FOREIGN KEY(student_id) REFERENCES students(id)
);
```
Endpoint upload banyak file
```python
# app.py
import os, sqlite3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/raw'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# init tables
with get_db() as db:
    # Tabel students
    db.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')

    # Tabel images
    db.execute('''CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        path TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    db.commit()

@app.post('/students')
def create_student():
    name = request.json.get('name')
    if not name:
        return jsonify({'error':'name required'}), 400
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO students(name) VALUES (?)', (name,))
    db.commit()
    sid = cur.lastrowid
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(sid)), exist_ok=True)
    return jsonify({'id': sid, 'name': name})

@app.post('/upload/<int:student_id>')
def upload_images(student_id):
    files = request.files.getlist('files')
    if not files or len(files) < 5:
        return jsonify({'error':'minimal 5 gambar'}), 400
    
    db = get_db()
    r = db.execute('SELECT id FROM students WHERE id=?', (student_id,)).fetchone()
    if not r:
        return jsonify({'error':'student not found'}), 404
    
    saved = []
    base = os.path.join(app.config['UPLOAD_FOLDER'], str(student_id))
    os.makedirs(base, exist_ok=True)

    for f in files:
        fname = secure_filename(f.filename)
        path = os.path.join(base, fname)
        f.save(path)
        db.execute('INSERT INTO images(student_id, path) VALUES (?,?)', (student_id, path))
        saved.append(path)
    db.commit()
    return jsonify({'student_id': student_id, 'saved': saved})

```
🎨 Frontend React (Vite)
Form upload multi-file
```jsx
// src/App.jsx
import { useState } from 'react';
import axios from 'axios';

export default function App() {
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

  return (
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
  );
}
```
Proxy dev ke Flask
```js
// vite.config.js
export default {
  server: {
    proxy: {
      '/students': 'http://localhost:5000',
      '/upload': 'http://localhost:5000'
    }
  }
}
```
🔄 Alur kerja
User isi nama siswa → klik Buat Siswa → backend buat record + folder.

User pilih ≥5 file gambar → klik Upload → semua gambar disimpan di folder siswa + path dicatat di tabel images.

Response JSON berisi daftar path gambar yang tersimpan.

## melihat daftar siswa beserta gambar-gambar mereka, lalu frontend bisa menampilkan hasilnya.

🛠 Backend Flask
Tambahkan endpoint /students_with_images:

```python
@app.get('/students_with_images')
def students_with_images():
    db = get_db()
    students = db.execute('SELECT id, name FROM students').fetchall()
    result = []
    for s in students:
        images = db.execute('SELECT id, path FROM images WHERE student_id=?', (s['id'],)).fetchall()
        result.append({
            'id': s['id'],
            'name': s['name'],
            'images': [dict(img) for img in images]
        })
    return jsonify(result)
```
👉 Output JSON contoh:

```json
[
  {
    "id": 1,
    "name": "Budi",
    "images": [
      {"id": 10, "path": "data/raw/1/budi1.jpg"},
      {"id": 11, "path": "data/raw/1/budi2.jpg"}
    ]
  },
  {
    "id": 2,
    "name": "Siti",
    "images": [
      {"id": 12, "path": "data/raw/2/siti1.jpg"}
    ]
  }
]
```
🎨 Frontend React (Vite)
Tambahkan tombol untuk fetch daftar siswa + gambar:

```jsx
// src/App.jsx
import { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    const { data } = await axios.get('http://localhost:5000/students_with_images');
    setStudents(data);
  };

  return (
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
  );
}
```
🔧 Catatan penting
Agar gambar bisa diakses dari frontend, tambahkan static file serving di Flask:

```python
from flask import send_from_directory

@app.get('/data/raw/<path:filename>')
def serve_image(filename):
    return send_from_directory('data/raw', filename)
```
Pastikan path yang disimpan di DB sesuai dengan route static ini (misalnya hanya student_id/filename.jpg).


## Tahap 3: Training data & save model. Di tahap ini kita akan mengambil gambar-gambar siswa dari SQLite, melakukan preprocessing, melatih model sederhana dengan TensorFlow/Keras, lalu menyimpan model ke disk agar bisa dipakai untuk prediksi nanti.

🛠 Backend Flask – Training Endpoint
1. Struktur dataset
Ambil semua gambar dari tabel images.

Label = student_id.

Preprocessing: resize ke 224×224, normalisasi sesuai model backbone (misalnya MobileNetV2).

2. Model sederhana
Gunakan MobileNetV2 pretrained sebagai feature extractor.

Tambahkan Dense layer dengan softmax sesuai jumlah siswa.

Freeze backbone untuk training cepat.

3. Endpoint /train
```python
# train.py (atau gabung di app.py)
import tensorflow as tf
import sqlite3, os, random, json
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras import layers, models

IMG_SIZE = (224, 224)

def get_dataset():
    conn = sqlite3.connect('students.db'); conn.row_factory = sqlite3.Row
    students = conn.execute('SELECT id, name FROM students').fetchall()
    id_to_idx = {s['id']: i for i,s in enumerate(students)}
    X, y = [], []
    for s in students:
        imgs = conn.execute('SELECT path FROM images WHERE student_id=?', (s['id'],)).fetchall()
        for row in imgs:
            X.append(row['path']); y.append(id_to_idx[s['id']])
    conn.close()
    # Shuffle
    idx = list(range(len(X))); random.shuffle(idx)
    X = [X[i] for i in idx]; y = [y[i] for i in idx]
    split = int(0.8 * len(X))
    return (X[:split], y[:split]), (X[split:], y[split:]), students, id_to_idx

def load_and_preprocess(path):
    img = tf.keras.utils.load_img(path, target_size=IMG_SIZE)
    arr = tf.keras.utils.img_to_array(img)
    return preprocess_input(arr)

def make_dataset(paths, labels, num_classes, batch=16):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    def _map(p, l):
        img = tf.numpy_function(load_and_preprocess, [p], tf.float32)
        img.set_shape((*IMG_SIZE, 3))
        return img, tf.one_hot(l, depth=num_classes)
    ds = ds.map(_map, num_parallel_calls=tf.data.AUTOTUNE)
    return ds.shuffle(512).batch(batch).prefetch(tf.data.AUTOTUNE)

def build_model(num_classes):
    base = MobileNetV2(include_top=False, weights='imagenet', input_shape=(*IMG_SIZE,3), pooling='avg')
    base.trainable = False
    x = layers.Dropout(0.2)(base.output)
    out = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(base.input, out)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

@app.post('/train')
def train_endpoint():
    (Xtr, ytr), (Xval, yval), students, id_to_idx = get_dataset()
    num_classes = len(students)
    if num_classes < 2:
        return jsonify({'error':'minimal 2 siswa untuk training'}), 400
    
    train_ds = make_dataset(Xtr, ytr, num_classes)
    val_ds = make_dataset(Xval, yval, num_classes)
    model = build_model(num_classes)
    history = model.fit(train_ds, validation_data=val_ds, epochs=5)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model.save('models/face_classifier.h5')
    with open('models/labels.json','w') as f:
        json.dump({v:k for k,v in id_to_idx.items()}, f)
    
    return jsonify({
        'epochs': 5,
        'train_acc': float(history.history['accuracy'][-1]),
        'val_acc': float(history.history['val_accuracy'][-1]),
        'classes': [{ 'id': s['id'], 'name': s['name']} for s in students]
    })
```
🎨 Frontend React – Tombol Training
Tambahkan tombol Train di interface:

```jsx
// src/App.jsx (lanjutan)
const trainModel = async () => {
  const { data } = await axios.post('http://localhost:5000/train');
  alert(`Training selesai. Val Acc: ${(data.val_acc*100).toFixed(1)}%`);
};

return (
  <div>
    {/* ...form upload sebelumnya... */}
    <hr/>
    <button onClick={trainModel}>Train Model</button>
  </div>
);
```
🔄 Alur Tahap 3
Backend ambil semua gambar dari DB.

Preprocessing → dataset train/val.

Model MobileNetV2 + Dense classifier dilatih.

Model disimpan ke folder models/face_classifier.h5 + label map JSON.

Frontend bisa trigger training dengan tombol.

## Tahap 4: Prediksi data. Di tahap ini kita akan membuat endpoint Flask untuk menerima gambar baru, melakukan preprocessing, memanggil model yang sudah disimpan, lalu mengembalikan hasil prediksi (nama siswa + probabilitas).

🛠 Backend Flask – Endpoint /predict
1. Load model & label map
Model disimpan di models/face_classifier.h5.

Label map di models/labels.json (mapping index → student_id).

Kita juga ambil nama siswa dari DB.

2. Endpoint prediksi
```python
import numpy as np, json
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load model dan label sekali di awal
model = load_model('models/face_classifier.h5')
with open('models/labels.json') as f:
    idx_to_student_id = {int(k): int(v) for k,v in json.load(f).items()}

def get_student_names():
    conn = sqlite3.connect('students.db'); conn.row_factory = sqlite3.Row
    names = {s['id']: s['name'] for s in conn.execute('SELECT id,name FROM students')}
    conn.close()
    return names

@app.post('/predict')
def predict():
    if 'file' not in request.files:
        return jsonify({'error':'file required'}), 400
    file = request.files['file']
    fname = secure_filename(file.filename)
    path = os.path.join('data','temp',fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)

    # Preprocess
    img = tf.keras.utils.load_img(path, target_size=(224,224))
    arr = tf.keras.utils.img_to_array(img)
    arr = preprocess_input(arr)
    logits = model.predict(arr[np.newaxis, ...])[0]

    # Ambil top-3 prediksi
    topk = np.argsort(logits)[::-1][:3]
    names = get_student_names()
    result = []
    for i in topk:
        sid = idx_to_student_id[i]
        result.append({
            'student_id': sid,
            'name': names[sid],
            'prob': float(logits[i])
        })
    return jsonify({'top': result})
```
🎨 Frontend React – Prediksi
Tambahkan input file untuk prediksi:

```jsx
// src/App.jsx (lanjutan)
const predictImage = async (file) => {
  const form = new FormData();
  form.append('file', file);
  const { data } = await axios.post('http://localhost:5000/predict', form);
  const best = data.top[0];
  alert(`Prediksi: ${best.name} (prob: ${(best.prob*100).toFixed(1)}%)`);
};

return (
  <div>
    {/* ...upload & train sebelumnya... */}
    <hr/>
    <h3>Prediksi Gambar Baru</h3>
    <input type="file" onChange={e => predictImage(e.target.files[0])}/>
  </div>
);
```
🔄 Alur Tahap 4
User upload gambar baru via frontend.

Backend /predict → load model + preprocessing → hasil softmax.

Backend kirim JSON top-3 prediksi (id, nama, probabilitas).

Frontend tampilkan hasil prediksi ke user.

👉 Dengan ini, pipeline sudah lengkap:

Upload data siswa (≥5 gambar).

Training model.

Save model.

Prediksi gambar baru.

## Tahap 5: Evaluasi data. Tujuan tahap ini adalah mengukur seberapa baik model mengenali wajah siswa, menemukan kesalahan prediksi, dan menyiapkan strategi perbaikan.

🛠 Backend Flask – Endpoint /evaluate
1. Ambil dataset validasi
Gunakan gambar yang sudah ada di DB (split train/val).

Jalankan model pada data validasi.

Hitung metrik: akurasi, confusion matrix, classification report.

2. Contoh implementasi
```python
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

@app.get('/evaluate')
def evaluate():
    # Ambil dataset validasi
    (_, _), (Xval, yval), students, id_to_idx = get_dataset()
    num_classes = len(students)
    if num_classes < 2:
        return jsonify({'error':'minimal 2 siswa'}), 400

    # Prediksi semua gambar validasi
    y_true, y_pred = [], []
    for path, label in zip(Xval, yval):
        img = tf.keras.utils.load_img(path, target_size=(224,224))
        arr = tf.keras.utils.img_to_array(img)
        arr = preprocess_input(arr)
        logits = model.predict(arr[np.newaxis, ...])[0]
        pred_idx = int(np.argmax(logits))
        y_true.append(label)
        y_pred.append(pred_idx)

    # Confusion matrix & report
    cm = confusion_matrix(y_true, y_pred).tolist()
    report = classification_report(y_true, y_pred, output_dict=True)

    return jsonify({
        'confusion_matrix': cm,
        'report': report
    })
```
👉 Output JSON berisi:

confusion_matrix: matriks NxN (N = jumlah siswa).

report: precision, recall, f1-score per kelas.

🎨 Frontend React – Menampilkan Evaluasi
Tambahkan tombol Evaluate:

```jsx
const evaluateModel = async () => {
  const { data } = await axios.get('http://localhost:5000/evaluate');
  console.log(data);
  alert(`Akurasi: ${(data.report.accuracy*100).toFixed(1)}%`);
};

return (
  <div>
    {/* ...upload, train, predict... */}
    <hr/>
    <button onClick={evaluateModel}>Evaluate Model</button>
  </div>
);
```

🔄 Alur Tahap 5
Backend jalankan model pada dataset validasi.

Hitung confusion matrix + classification report.

Frontend tampilkan akurasi dan metrik.

User bisa melihat siswa mana yang sering salah diprediksi.

📈 Strategi Perbaikan
Tambah data sulit: foto dengan pencahayaan berbeda, ekspresi beragam.

Augmentasi: flip, zoom, brightness.

Fine-tuning: buka beberapa layer terakhir MobileNetV2.

Balance dataset: pastikan tiap siswa punya jumlah gambar seimbang.

Face detection crop: gunakan endpoint crop agar dataset lebih bersih.

👉 Dengan ini pipeline lengkap:

Upload data siswa.

Training model.

Save model.

Prediksi gambar baru.

Evaluasi & perbaikan.

## Tahap 6: Perbaikan prediksi dengan menambah data baru. Konsep utamanya: model machine learning akan lebih baik jika dataset bertambah dan lebih beragam. Jadi ketika hasil prediksi kurang baik, kita lakukan data enrichment lalu retraining.

🔄 Alur Tahap 6
Evaluasi hasil prediksi

Gunakan endpoint /evaluate untuk melihat confusion matrix dan laporan akurasi.

Identifikasi siswa yang sering salah diprediksi.

Tambah data baru

Upload gambar tambahan untuk siswa yang sering salah dikenali.

Pastikan gambar baru memiliki variasi: pencahayaan berbeda, sudut wajah, ekspresi, aksesoris (kacamata, masker).

Gunakan endpoint /upload/<student_id> untuk menambahkan gambar baru ke DB.

Update dataset

Setelah gambar baru masuk, dataset otomatis bertambah.

Tidak perlu menghapus data lama, cukup tambahkan data baru agar distribusi lebih seimbang.

Retraining model

Jalankan kembali endpoint /train.

Model akan dilatih ulang dengan dataset yang sudah diperbarui.

Simpan model baru (face_classifier.h5) menggantikan versi lama.

Prediksi ulang

Gunakan endpoint /predict dengan gambar uji baru.

Bandingkan hasil prediksi sebelum dan sesudah retraining.

🛠 Contoh Flow di Backend
```python
# Tambah gambar baru untuk siswa tertentu
@app.post('/upload/<int:student_id>')
def upload_images(student_id):
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error':'minimal 1 gambar'}), 400
    db = get_db()
    r = db.execute('SELECT id FROM students WHERE id=?', (student_id,)).fetchone()
    if not r: return jsonify({'error':'student not found'}), 404
    saved = []
    base = os.path.join(app.config['UPLOAD_FOLDER'], str(student_id))
    os.makedirs(base, exist_ok=True)
    for f in files:
        fname = secure_filename(f.filename)
        path = os.path.join(base, fname)
        f.save(path)
        db.execute('INSERT INTO images(student_id, path) VALUES (?,?)', (student_id, path))
        saved.append(path)
    db.commit()
    return jsonify({'student_id': student_id, 'saved': saved})
```
👉 Setelah upload tambahan, panggil /train lagi untuk retraining.

🎨 Frontend Flow
Tambahkan tombol Upload tambahan di halaman siswa.

Setelah upload, tampilkan jumlah total gambar siswa.

Tambahkan tombol Retrain agar user bisa melatih ulang model dengan dataset terbaru.

📈 Strategi Perbaikan
Data Augmentation: selain menambah gambar manual, gunakan augmentasi otomatis (flip, zoom, brightness).

Fine-tuning: buka beberapa layer terakhir MobileNetV2 agar model belajar lebih spesifik ke dataset.

Balance dataset: pastikan setiap siswa punya jumlah gambar relatif sama.

Iterasi: ulangi siklus → evaluasi → tambah data → retrain → prediksi ulang.

## Struktur Folder
```Code
face-recognition-app/
│
├── backend/
│   ├── app.py                # Flask backend utama
│   ├── train.py              # Fungsi training model
│   ├── students.db           # SQLite database
│   ├── models/
│   │   ├── face_classifier.h5 # Model tersimpan
│   │   └── labels.json        # Mapping label
│   └── data/
│       ├── raw/              # Folder gambar siswa
│       │   ├── 1/            # Gambar siswa id=1
│       │   └── 2/            # Gambar siswa id=2
│       └── temp/             # Temp upload/prediksi
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # React interface
│   │   └── main.jsx
│   ├── vite.config.js        # Proxy ke backend
│   └── package.json
│
└── requirements.txt          # Python dependencies
```