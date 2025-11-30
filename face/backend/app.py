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

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "MNIST Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
