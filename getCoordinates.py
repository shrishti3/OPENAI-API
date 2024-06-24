import openai
import base64
import requests
import json
# Initialize OpenAI API
openai.api_key = API_KEY

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def getCoordinates(image_path):
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
          "text": "Let left corner of image be (0,0), return list of coordinates of bounding blocks rectangle of all texts with 5px of padding each side. the output string should follow json format and can be parsed. the format is, create an array of objects that contain the text it stores and a 2d array for coordinates.The output shound not contain any information apart from the text and coordinates. strictly follow these rules. the output should not contain json or ```"
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
  max_tokens=400
  )
#   json.loads(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)
   
  