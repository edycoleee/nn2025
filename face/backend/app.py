from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, sqlite3, random, json
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras import layers, models
import numpy as np, json
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

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

@app.get('/data/raw/<path:filename>')
def serve_image(filename):
    return send_from_directory('data/raw', filename)

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
    base = MobileNetV2(include_top=False, weights='imagenet',
                       input_shape=(*IMG_SIZE,3), pooling='avg')
    # Fine-tune sebagian layer
    for layer in base.layers[:-20]:
        layer.trainable = False

    x = layers.Dense(256, activation='relu')(base.output)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    out = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(base.input, out)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
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

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "FACE RECOGNITION Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
