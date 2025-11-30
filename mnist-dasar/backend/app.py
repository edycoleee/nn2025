from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_image

app = Flask(__name__)
CORS(app)

model = load_model("model/mnist_cnn.h5")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    img_bytes = file.read()
    processed = preprocess_image(img_bytes)
    
    preds = model.predict(processed)
    class_id = int(preds.argmax())
    confidence = float(preds.max())
    
    return jsonify({"digit": class_id, "confidence": confidence})

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "MNIST Flask API is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
