from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Load the tokenizer and model
model_name = "loganbarnhart/starcoder-tex"
tokenizer_name = "bigcode/starcoderbase-1b"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Generate text
def generate_text(prompt, max_length=50, num_return_sequences=1):
    start = 'Please translate the following natural language into LaTeX code:\nNatural language:'
    prompt = start + prompt + '\nLatex:$$'
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

@app.route('/generate', methods=['POST'])
def generate_api():
    data = request.get_json()
    prompt = data['prompt']
    max_length = data.get('max_length', 50)
    num_return_sequences = data.get('num_return_sequences', 1)

    generated_text = generate_text(prompt, max_length, num_return_sequences)
    response = {'generated_text': generated_text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
