from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def main():
  
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  tokenizer = AutoTokenizer.from_pretrained('gpt2')
  model = AutoModelForCausalLM.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id).to(device)

  input = "Hello! What do you think about LaTeX?"
  tokenized_input = tokenizer(input, return_tensors='pt').to(device)
  output = model.generate(**tokenized_input, max_new_tokens=50)
  print(f"Input: {input}\n")
  print("-"*50 + "Test Output" + "-"*50)
  print(tokenizer.decode(output[0], skip_special_tokens = True))
