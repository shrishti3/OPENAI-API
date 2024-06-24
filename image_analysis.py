import openai
import base64
import requests
# Initialize OpenAI API
openai.api_key = API_KEY

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image(image_path):
    # encode image to base64
    base64_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
       model="gpt-4o",
        messages= [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Detect all text in the image and list it down, do not include any cta elements in this. "
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  max_tokens=100
  )
    return response.choices[0].message.content
  