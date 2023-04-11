from flask import Flask, request
from flask_cors import CORS
import os, json
from ast import literal_eval
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# model_list = openai.Model.list()

app = Flask(__name__)
CORS(app)

def get_gpt_response(final_prompt):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": final_prompt}],
        max_tokens=700,
        temperature=0.7,
        stream=False
        )

        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def modify_prompt(idea, structure):
    try:
        with open('rules.txt', 'r') as f:
            rules_prompt = f.read()
    except:
        pass
    template_prompt = f"""This is the business model structure:
```
{structure}
```"""
    idea_prompt = f"The idea is [{idea}]"
    rules_dict = {}
    rules_prompt += ''
    for d in structure:
        rules_dict.update({d['name']:"content"})
    rules_prompt += f'[{rules_dict}]\nThe response:'
    return f"{template_prompt}\n{idea_prompt}\n{rules_prompt}"

@app.route('/get_result', methods=['POST'])
def get_idea_sirji():
    idea = request.json.get('inputText')
    with open('business_structure.json', 'r') as f:
            structure = json.load(f)
    len_structure = len(structure)
    prompt_with_idea = modify_prompt(idea, structure)
    print(f"\nPrompt: {prompt_with_idea}\n\n")
    gpt_response =  get_gpt_response(prompt_with_idea)
    output_text = gpt_response['choices'][0]['message']['content']
    finish_reason = gpt_response['choices'][0]['finish_reason']
    if finish_reason == 'stop':
        print("\nValid response in first attempt!\n")

    if finish_reason == 'length':
        print("\nInvalid response in First attempt, Splitting business structure for another shot.\n")
        while finish_reason!='stop':
            response_list = []
            for i in range(0, len_structure+1, len_structure//2):
                print(f"{i}, {(i+len_structure//2)+1}")
                prompt_with_idea = modify_prompt(idea, structure[i:(i+len_structure//2)+1])
                gpt_response =  get_gpt_response(prompt_with_idea)
                print(gpt_response)
                output_text = gpt_response['choices'][0]['message']['content']
                finish_reason = gpt_response['choices'][0]['finish_reason']
                response_list.extend(literal_eval(output_text.replace("'", "\""))[0])
            print(response_list)
            return response_list[0]
    elif finish_reason == 'stop':
        print(gpt_response)
        return literal_eval(output_text.replace("'", "\""))[0]

if __name__ == '__main__':
    app.run(debug=True)