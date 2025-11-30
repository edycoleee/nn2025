from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sqlite3
from werkzeug.utils import secure_filename

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

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "MNIST Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
