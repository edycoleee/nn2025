import sqlite3
import os

def init_db():
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()
    
    # Table untuk kelas/target
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table untuk gambar training
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS training_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        image_data BLOB,
        filename TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes (id)
    )
    ''')
    
    # Table untuk model yang sudah di-train
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trained_models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        model_path TEXT,
        accuracy REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('dataset.db')
    conn.row_factory = sqlite3.Row
    return conn