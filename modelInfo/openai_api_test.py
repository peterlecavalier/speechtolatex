from openai import OpenAI

def load_dataset(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tex_lines = file.readlines()
    return [line.strip() for line in tex_lines]

def translate(tex_lines):
    translations = []
    for line in tex_lines:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",

            #prompt=f'' ,
            ### TODO: INPUT PROMPT, CHECK WHETHER OR NOT YOU NEED ADDITIONAL \ BEFORE 
            ### COMMANDS LIKE \begin, \end, \frac{}{}, etc. 

            temperature=0.4,
            max_tokens=200
        )
        translations.append(response.choices[0].text.strip())
    return translations

### Testing a few responses:

#client = OpenAI()

test_prompt='Translate the following LaTeX equations into natural language:\n\nLaTeX: `\\begin{align*} x^2 + y^2 = z^2 \end{align*}`\nNatural Language: "The sum of x squared plus y squared equals z squared."\n\nLaTeX: `\\frac{d}{dx} x^2`\nNatural Language: "The derivative of x squared with respect to x."\n\nLaTeX: `R _ { 1 2 } K _ { 1 } R _ { 2 1 } d K _ { 2 } = d K _ { 2 } R _ { 1 2 } K _ { 1 } R _ { 1 2 } ^ { - 1 }`\nNatural Language:'

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo-instruct",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": test_prompt}    
  ],
  temperature=0.4,
  max_tokens=200
)

print(response)
print('-'*50)
print(response['choices'])
print('-'*50)
print(response['choices'][0]['text'])
print('-'*50)
print(response['usage'])

