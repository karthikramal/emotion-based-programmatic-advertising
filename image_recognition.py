import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

def load_and_prepare_image(file_path):
    img = image.load_img(file_path, target_size=(224, 224))  # Load and resize the image
    img_array = image.img_to_array(img)  # Convert the image to a numpy array
    img_array_expanded = np.expand_dims(img_array, axis=0)  # Add an extra dimension for batch size
    return preprocess_input(img_array_expanded)  # Preprocess the image as required by MobileNetV2

def recognize_image(file_path):
    model = MobileNetV2(weights='imagenet')  # Load the pre-trained MobileNetV2 model
    img_processed = load_and_prepare_image(file_path)  # Load and preprocess the image
    predictions = model.predict(img_processed)  # Make predictions
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Decode predictions into readable class names
    return decoded_predictions  # Return the top 3 predictions

# Example usage
file_path = 'path/to/your/image.jpg'  # Replace with the path to your image file
predictions = recognize_image(file_path)
for i, (imagenet_id, label, score) in enumerate(predictions):
    print(f"{i + 1}: {label} ({score:.2f})")
