import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from database import get_db_connection
import os
from datetime import datetime
import pickle

class ModelTrainer:
    def __init__(self):
        self.img_height = 224
        self.img_width = 224
        self.num_channels = 3
        
    def prepare_data_from_db(self):
        """Menyiapkan data training dari database SQLite"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ambil semua gambar dan label
        cursor.execute('''
            SELECT ti.image_data, c.class_name
            FROM training_images ti
            JOIN classes c ON ti.class_id = c.id
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return None, None, None
        
        images = []
        labels = []
        class_names = []
        
        for row in rows:
            # Decode image dari BLOB
            nparr = np.frombuffer(row['image_data'], np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                # Resize dan normalize
                img = cv2.resize(img, (self.img_height, self.img_width))
                img = img / 255.0
                images.append(img)
                
                # Simpan label
                class_name = row['class_name']
                if class_name not in class_names:
                    class_names.append(class_name)
                
                labels.append(class_names.index(class_name))
        
        if not images:
            return None, None, None
            
        # Convert ke numpy array
        X = np.array(images)
        y = np.array(labels)
        
        # One-hot encoding
        y_onehot = tf.keras.utils.to_categorical(y, num_classes=len(class_names))
        
        return X, y_onehot, class_names
    
    def create_model(self, num_classes):
        """Membuat model CNN sederhana"""
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, self.num_channels)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, epochs=10):
        """Melakukan training model"""
        # Persiapan data
        X, y, class_names = self.prepare_data_from_db()
        
        if X is None:
            return {'success': False, 'error': 'No training data found'}
        
        # Split data (80% training, 20% validation)
        split_idx = int(len(X) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Buat model
        model = self.create_model(len(class_names))
        
        # Training
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            validation_data=(X_val, y_val),
            batch_size=32
        )
        
        # Evaluasi
        val_loss, val_accuracy = model.evaluate(X_val, y_val)
        
        # Simpan model
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"model_{timestamp}"
        model_path = f"data/models/{model_name}.h5"
        labels_path = f"data/models/labels_{timestamp}.txt"
        
        # Buat folder jika belum ada
        os.makedirs("data/models", exist_ok=True)
        
        # Simpan model
        model.save(model_path)
        
        # Simpan labels
        with open(labels_path, 'w') as f:
            for class_name in class_names:
                f.write(f"{class_name}\n")
        
        # Simpan class names untuk mapping
        class_mapping_path = f"data/models/class_mapping_{timestamp}.pkl"
        with open(class_mapping_path, 'wb') as f:
            pickle.dump(class_names, f)
        
        return {
            'success': True,
            'model_name': model_name,
            'model_path': model_path,
            'labels_path': labels_path,
            'class_mapping_path': class_mapping_path,
            'accuracy': float(val_accuracy),
            'loss': float(val_loss),
            'num_classes': len(class_names),
            'num_samples': len(X)
        }