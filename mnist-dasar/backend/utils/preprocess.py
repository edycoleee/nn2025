import numpy as np
from PIL import Image
import io

def preprocess_image(image_bytes, target_size=(28,28)):
    img = Image.open(io.BytesIO(image_bytes)).convert("L")  # grayscale
    img = img.resize(target_size)
    img_array = np.array(img).astype("float32") / 255.0
    img_array = np.expand_dims(img_array, axis=-1)  # shape (28,28,1)
    return np.expand_dims(img_array, axis=0)        # shape (1,28,28,1)
