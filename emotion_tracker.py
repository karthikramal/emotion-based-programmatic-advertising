import requests
import json

# Assume the following functions are defined and implemented:
# analyze_post_text(text): Returns analysis of the post text
# analyze_image(file_path): Returns a description and summary of an image
# analyze_video(file_path): Returns a summary of a video

# Example inputs
post_text = "Your post text here"
file_path = "path/to/your/image/or/video"
is_video = False  # Set to True if the file is a video

# Analyze the post text
post_text_analysis = analyze_post_text(post_text)

# Analyze the image or video
if is_video:
    video_summary = analyze_video(file_path)
    combined_info = f"Post Text: {post_text_analysis}\nVideo Summary: {video_summary}"
else:
    image_description, image_summary = analyze_image(file_path)
    combined_info = f"Post Text: {post_text_analysis}\nImage Description: {image_description}\nImage Summary: {image_summary}"

# Formulate the request to ChatGPT
request_to_chatgpt = f"{combined_info}\nBased on this ad content, what emotions and situations might a customer experience?"

# Define the API endpoint and your API key for ChatGPT
api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
headers = {
    "Authorization": f"Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Prepare the data payload for the API request
data = {
    "prompt": request_to_chatgpt,
    "max_tokens": 200
}

# Make the API request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Check if the request was successful and get the response
if response.status_code == 200:
    chatgpt_response = response.json()["choices"][0]["text"]
    print("ChatGPT's Analysis:", chatgpt_response)
else:
    print("Error in API request:", response.text)
