from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from datetime import datetime
import pickle

from database import init_db
from models import ClassManager, ImageManager, ModelManager
from train_model import ModelTrainer

# Initialize
app = Flask(__name__)
CORS(app)
init_db()

# Global variables untuk model yang sedang aktif
current_model = None
current_labels = []
class_mapping = []

def load_active_model():
    """Load model yang active dari database"""
    global current_model, current_labels, class_mapping
    
    model_info = ModelManager.get_active_model()
    if model_info:
        try:
            from tensorflow import keras
            current_model = keras.models.load_model(model_info['model_path'])
            
            # Load labels
            model_dir = os.path.dirname(model_info['model_path'])
            timestamp = model_info['model_name'].split('_')[1]
            labels_path = f"{model_dir}/labels_{timestamp}.txt"
            mapping_path = f"{model_dir}/class_mapping_{timestamp}.pkl"
            
            with open(labels_path, 'r') as f:
                current_labels = [line.strip() for line in f.readlines()]
            
            with open(mapping_path, 'rb') as f:
                class_mapping = pickle.load(f)
            
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    return False

# Load model saat startup
load_active_model()

@app.route('/api/classes', methods=['GET', 'POST', 'DELETE'])
def manage_classes():
    """CRUD untuk kelas"""
    if request.method == 'GET':
        classes = ClassManager.get_all_classes()
        return jsonify([dict(cls) for cls in classes])
    
    elif request.method == 'POST':
        data = request.json
        class_name = data.get('class_name')
        
        if not class_name:
            return jsonify({'success': False, 'error': 'Class name required'})
        
        class_id = ClassManager.add_class(class_name)
        if class_id:
            return jsonify({'success': True, 'class_id': class_id})
        else:
            return jsonify({'success': False, 'error': 'Class already exists'})
    
    elif request.method == 'DELETE':
        class_id = request.args.get('id')
        if class_id:
            ClassManager.delete_class(class_id)
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Class ID required'})

@app.route('/api/images', methods=['POST'])
def upload_image():
    """Upload gambar untuk training"""
    try:
        data = request.json
        class_id = data['class_id']
        image_data = data['image'].split(',')[1]
        filename = data.get('filename', f'image_{datetime.now().timestamp()}.jpg')
        
        # Decode base64
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        
        # Save ke database
        image_id = ImageManager.save_image(class_id, nparr.tobytes(), filename)
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'filename': filename
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/train', methods=['POST'])
def train_model():
    """Endpoint untuk training model baru"""
    try:
        data = request.json
        epochs = data.get('epochs', 10)
        
        trainer = ModelTrainer()
        result = trainer.train(epochs=epochs)
        
        if result['success']:
            # Save model info ke database
            ModelManager.save_model_info(
                result['model_name'],
                result['model_path'],
                result['accuracy']
            )
            
            # Reload model yang baru
            load_active_model()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint untuk prediksi dengan model yang aktif"""
    try:
        if current_model is None:
            load_active_model()
            if current_model is None:
                return jsonify({'success': False, 'error': 'No model available'})
        
        data = request.json
        image_data = data['image'].split(',')[1]
        
        # Decode base64
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Preprocess
        image = cv2.resize(image, (224, 224))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Predict
        predictions = current_model.predict(image, verbose=0)
        index = np.argmax(predictions[0])
        confidence = float(predictions[0][index] * 100)
        
        # Get class name dari mapping
        if index < len(class_mapping):
            class_name = class_mapping[index]
        else:
            class_name = f"Class {index}"
        
        return jsonify({
            'success': True,
            'prediction': class_name,
            'confidence': confidence,
            'all_predictions': predictions[0].tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list semua model yang pernah di-train"""
    models = ModelManager.get_all_models()
    return jsonify([dict(model) for model in models])

@app.route('/api/switch-model', methods=['POST'])
def switch_model():
    """Switch ke model tertentu"""
    try:
        model_id = request.json.get('model_id')
        # Implementasi switch model
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "MODEL RECOGNITION Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
