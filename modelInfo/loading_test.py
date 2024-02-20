# import transformers
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import bitsandbytes
# import accelerate
# 
# from peft import (
#   LoraConfig,
#   PeftConfig,
#   PeftModel,
#   get_peft_model,
#   prepare_model_for_kbit_training,
# )
# 
# from transformers import (
#   AutoTokenizer,
#   AutoConfig,
#   AutoModelForCausalLM,
#   AutoModelForSequenceClassification,
#   BitsAndBytesConfig,
#   Trainer,
# )

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


 # MODEL_NAME = "meta-llama/Llama-2-7b-hf"
 # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
 # tokenizer.pad_token = tokenizer.eos_token

 # model = AutoModelForCausalLM.from_pretrained(
 #   MODEL_NAME,
 #   device_map = 'auto',
 #   trust_remote_code = True,
 #   quantization_config = bnb_config
 # )

 # model = get_peft_model(model, lora_config)
 # print_trainable_parameters(model)

# bnb_config = BitsAndBytesConfig(
#   load_in_4bit = True,
#   bnb_4bit_use_double_quant = True,
#   bnb_4bit_quant_type = 'nf4',
#   bnb_4bit_compute_dtype = torch.bfloat16
# )
# 
# lora_config = LoraConfig(
#   r = 16,
#   lora_alpha = 32,
#   target_modules = ["q_proj", "v_proj"],
#   lora_dropout = 0.05,
#   bias = 'none',
#   task_type = 'causal_LM'
# )

if __name__ == "__main__":
  main()
