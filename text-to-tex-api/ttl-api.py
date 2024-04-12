import openai
import os
from openai import OpenAI
from flask import Flask, request, jsonify
from google.cloud import secretmanager

app = Flask(__name__)

project_id = 'curious-destiny-414303'
secret_id = "openai-api-key"

def access_secret_version(secret_id, version_id='latest'):
  client = secretmanager.SecretManagerServiceClient()
  name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
  response = client.access_secret_version(request = {"name":name})
  return response.payload.data.decode("UTF-8")

api_key = access_secret_version(secret_id)

client = OpenAI(api_key = api_key)

@app.route('/translate', methods=['POST'])
def translate():
  if 'text' not in request.json:
    return jsonify({'error': 'No text provided'}), 400
  
  text = request.json['text']

  prompt_start = 'Translate the following text into LaTeX.\nText: The derivative of y with respect to x is eight x e to the four x squared.\nLaTeX: \\frac{dy}{dx} = 8xe^{4x^2}\nText: y prime equals 4 y\nLaTeX: y\' = 4y\nText: '

  prompt = prompt_start + text + '\nLaTeX: '

  response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0.2,
    max_tokens=1000)

  latex_code = response.choices[0].text

  return jsonify({'latex': latex_code}), 200

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(debug=True, host='0.0.0.0', port = port)
