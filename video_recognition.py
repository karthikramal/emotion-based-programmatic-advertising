import cv2
import tensorflow as tf
import speech_recognition as sr
from pydub import AudioSegment
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def load_and_prepare_image(img):
    img_array = image.img_to_array(img)  # Convert the image to a numpy array
    img_array_expanded = np.expand_dims(img_array, axis=0)  # Add an extra dimension for batch size
    return preprocess_input(img_array_expanded)  # Preprocess the image as required by MobileNetV2

def recognize_frame(frame, model):
    img_processed = load_and_prepare_image(frame)  # Preprocess the frame
    predictions = model.predict(img_processed)  # Make predictions
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Decode predictions into readable class names
    return decoded_predictions  # Return the top 3 predictions

def extract_audio(video_path, audio_path='temp_audio.wav'):
    video = AudioSegment.from_file(video_path, "mp4")
    video.export(audio_path, format="wav")
    return audio_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Audio was not understood"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

def analyze_video(video_path, frame_rate=1):
    # Initialize the video frame recognition model
    model = MobileNetV2(weights='imagenet')

    # Process video frames
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    video_analysis = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if frame_count % (30 // frame_rate) == 0:  # Process frames at the specified frame rate
            predictions = recognize_frame(frame, model)
            frame_desc = f"Frame {frame_count}: " + ", ".join([f"{label} ({score:.2f})" for _, label, score in predictions])
            video_analysis.append(frame_desc)

        frame_count += 1

    cap.release()

    # Extract and transcribe audio
    audio_path = extract_audio(video_path)
    audio_transcription = transcribe_audio(audio_path)
    os.remove(audio_path)  # Clean up the temporary audio file

    return video_analysis, audio_transcription

# Example usage
video_path = 'path/to/your/video.mp4'  # Replace with the path to your video file
video_summary, audio_transcript = analyze_video(video_path, frame_rate=1)

print("Video Summary:\n", "\n".join(video_summary))
print("\nAudio Transcription:\n", audio_transcript)
