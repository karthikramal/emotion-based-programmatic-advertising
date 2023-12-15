import cv2
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

def load_and_prepare_image(img):
    img_array = image.img_to_array(img)  # Convert the image to a numpy array
    img_array_expanded = np.expand_dims(img_array, axis=0)  # Add an extra dimension for batch size
    return preprocess_input(img_array_expanded)  # Preprocess the image as required by MobileNetV2

def recognize_frame(frame):
    model = MobileNetV2(weights='imagenet')  # Load the pre-trained MobileNetV2 model
    img_processed = load_and_prepare_image(frame)  # Preprocess the frame
    predictions = model.predict(img_processed)  # Make predictions
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Decode predictions into readable class names
    return decoded_predictions  # Return the top 3 predictions

def recognize_video(video_path, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    model = MobileNetV2(weights='imagenet')  # Load the model outside the frame processing loop
    success, frame = cap.read()
    frame_count = 0

    while success:
        if frame_count % (30 // frame_rate) == 0:  # Process frames at the specified frame rate
            decoded_predictions = recognize_frame(frame)
            print(f"Frame {frame_count}:")
            for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
                print(f"  {i + 1}: {label} ({score:.2f})")
            print("\n")

        success, frame = cap.read()
        frame_count += 1

    cap.release()

# Example usage
video_path = 'path/to/your/video.mp4'  # Replace with the path to your video file
recognize_video(video_path, frame_rate=1)  # Analyze one frame per second
