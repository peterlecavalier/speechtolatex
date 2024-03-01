from openai import OpenAI

def main():

    ### Testing a few responses:

    # test_prompt='Translate the following LaTeX equations into natural language:\n\nLaTeX: `\\begin{align*} x^2 + y^2 = z^2 \end{align*}`\nNatural Language: "The sum of x squared plus y squared equals z squared."\n\nLaTeX: `\\3 frac{d}{dx} x^2`\nNatural Language: "Three times the derivative of x squared with respect to x."\n\nLaTeX: `R _ { 1 2 } K _ { 1 } R _ { 2 1 } d K _ { 2 } = d K _ { 2 } R _ { 1 2 } K _ { 1 } R _ { 1 2 } ^ { - 1 }`\nNatural Language:'

    # client = OpenAI()

    # response = client.completions.create(
    #   model="gpt-3.5-turbo-instruct",
    #   prompt=test_prompt,
    #   temperature=0.4,
    #   max_tokens=200
    # )

    # print(response)
    # print('-'*50)
    # print(response.choices)
    # print('-'*50)
    # print(response.choices[0].text)
    # print('-'*50)
    # print(response.usage)

    data = load_dataset('data/formulas_subset_small.txt')
    translations = translate(data)
    write_to_file(translations, 'data/subset_translations_small.txt')

def load_dataset(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tex_lines = file.readlines()
    return [line.strip() for line in tex_lines]

def translate(tex_lines):
    translations = []
    client = OpenAI()
    prompt_start = 'Translate the following LaTeX equations into natural language:\n\nLaTeX: `\\begin{align*} \hat{x}^2 + (y^*)^2 = \\tilde{z}^2 \end{align*}`\nNatural Language: "The sum of x hat squared plus y star squared equals z tilde squared."\n\nLaTeX: `\\3 frac{d}{dx} x^2`\nNatural Language: "Three times the derivative of x squared with respect to x."\n\nLaTeX:'
    for line in tex_lines:
        full_prompt = f'{prompt_start}{line}\nNatural Language:'
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",

            prompt= full_prompt,

            temperature=0.4,
            max_tokens=200
        )
        translations.append(response.choices[0].text.strip())
    return translations

def write_to_file(text_list, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        for text in text_list:
            file.write(text + '\n')

if __name__ == "__main__":
    main()