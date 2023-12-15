import requests
import json

# Assuming recognize_image is a function that returns a list of recognized objects and their descriptions
image_descriptions = recognize_image("path/to/image.jpg")

# Format the data into a coherent description for sending to ChatGPT
formatted_data = f"I have an image with the following objects and features: {', '.join(image_descriptions)}. Can you provide a detailed scenario description and summary based on these elements?"

# Define the API endpoint and your API key for ChatGPT
api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
headers = {
    "Authorization": f"Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# Prepare the data payload for the API request
data = {
    "prompt": formatted_data,
    "max_tokens": 150  # Adjust based on how detailed you want the response
}

# Make the API request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Check if the request was successful and get the response
if response.status_code == 200:
    scenario_description = response.json()["choices"][0]["text"]
    print("Scenario Description and Summary:", scenario_description)
else:
    print("Error in API request:", response.text)

