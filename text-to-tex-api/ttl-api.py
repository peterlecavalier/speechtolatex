import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO: SET UP GCP SECRET MANAGER STORE OAI API KEY AND ACCESS IT HERE WHEN DEPLOYING
openai.api_key = 0000

client = OpenAI()

@app.route('/translate', methods=['POST'])
def translate():
  if text not in request.json:
    return jsonify({'error': 'No text provided'}), 400
  
  text = request.json['text']

  prompt_start = 'Translate the following text into LaTeX.\nText: The derivative of y with respect to x is eight x e to the four x squared.\nLaTeX: \\frac{dy}{dx} = 8xe^{4x^2}\nText: y prime equals 4 y\nLaTeX: y' = 4y\nText: '

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
