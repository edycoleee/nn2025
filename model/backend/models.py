from database import get_db_connection

class ClassManager:
    @staticmethod
    def add_class(class_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO classes (class_name) VALUES (?)', (class_name,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all_classes():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classes ORDER BY class_name')
        classes = cursor.fetchall()
        conn.close()
        return classes
    
    @staticmethod
    def delete_class(class_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM classes WHERE id = ?', (class_id,))
        cursor.execute('DELETE FROM training_images WHERE class_id = ?', (class_id,))
        conn.commit()
        conn.close()

class ImageManager:
    @staticmethod
    def save_image(class_id, image_data, filename):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO training_images (class_id, image_data, filename) 
            VALUES (?, ?, ?)
        ''', (class_id, image_data, filename))
        conn.commit()
        image_id = cursor.lastrowid
        conn.close()
        return image_id
    
    @staticmethod
    def get_images_by_class(class_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM training_images 
            WHERE class_id = ? 
            ORDER BY created_at DESC
        ''', (class_id,))
        images = cursor.fetchall()
        conn.close()
        return images
    
    @staticmethod
    def get_all_images_for_training():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ti.image_data, c.class_name
            FROM training_images ti
            JOIN classes c ON ti.class_id = c.id
        ''')
        data = cursor.fetchall()
        conn.close()
        return data

class ModelManager:
    @staticmethod
    def save_model_info(model_name, model_path, accuracy):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Set semua model menjadi non-active
        cursor.execute('UPDATE trained_models SET status = "inactive"')
        # Simpan model baru sebagai active
        cursor.execute('''
            INSERT INTO trained_models (model_name, model_path, accuracy, status)
            VALUES (?, ?, ?, "active")
        ''', (model_name, model_path, accuracy))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_active_model():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trained_models WHERE status = "active" ORDER BY created_at DESC LIMIT 1')
        model = cursor.fetchone()
        conn.close()
        return model
    
    @staticmethod
    def get_all_models():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trained_models ORDER BY created_at DESC')
        models = cursor.fetchall()
        conn.close()
        return models