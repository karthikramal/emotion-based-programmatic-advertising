import mimetypes
from image_recognition import process_image
from video_recognition import process_video

def main(file_path):
    # Determine the type of the file based on MIME type
    file_type, _ = mimetypes.guess_type(file_path)

    if file_type is not None:
        if file_type.startswith('image'):
            return process_image(file_path)
        elif file_type.startswith('video'):
            return process_video(file_path)
        else:
            return "File is neither an image nor a video"
    else:
        return "Unable to determine the file type"

# Example usage
file_path = 'path/to/your/file'  # Replace with the path to your image or video file
result = main(file_path)
print(result)
