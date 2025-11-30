from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
model = load_model("mnist_model.h5")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    img_data = data['image']  # base64 string

    # Decode base64 ke image
    img_bytes = base64.b64decode(img_data.split(',')[1])
    img = Image.open(io.BytesIO(img_bytes)).convert('L').resize((28,28))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1,28,28)

    prediction = model.predict(img_array)
    label = int(np.argmax(prediction))

    return jsonify({"prediction": label})

if __name__ == '__main__':
    app.run(debug=True)
