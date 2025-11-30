# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Izinkan semua origin (bisa dibatasi nanti)

# Load model CIFAR
model = load_model("model/cifar_model.h5")
class_names = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((32, 32))  # CIFAR ukuran 32x32
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    img_bytes = file.read()
    processed = preprocess_image(img_bytes)
    
    preds = model.predict(processed)
    class_id = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))
    
    return jsonify({
        "class": class_names[class_id],
        "confidence": confidence
    })

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
