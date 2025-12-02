# CNN untuk MNIST 
import tensorflow as tf 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense 
from tensorflow.keras.utils import to_categorical 

# 1. Load dataset 
(x_train, y_train), (x_test, y_test) = mnist.load_data() 
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0 
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0 

y_train = to_categorical(y_train, 10) 
y_test = to_categorical(y_test, 10) 

# 2. Bangun CNN 

model = Sequential([ 
    Conv2D(32, kernel_size=(3,3), activation="relu", input_shape=(28,28,1)), 
    MaxPooling2D(pool_size=(2,2)), 
    Conv2D(64, kernel_size=(3,3), activation="relu"), 
    MaxPooling2D(pool_size=(2,2)), 
    Flatten(), 
    Dense(128, activation="relu"), 
    Dense(10, activation="softmax") 
]) 

 

# 3. Compile & train 

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]) 
history = model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1) 
 

# 4. Evaluasi 
test_loss, test_acc = model.evaluate(x_test, y_test) 
print("Test accuracy CNN:", test_acc) 

# Simpan model
model.save("mnist_model.h5")
