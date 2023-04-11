from flask import Flask, request
from flask_cors import CORS
import os, json
from ast import literal_eval
import openai
import threading

openai.api_key = os.getenv("OPENAI_API_KEY")
# model_list = openai.Model.list()

app = Flask(__name__)
CORS(app)

def get_gpt_response(final_prompt):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": final_prompt}],
        max_tokens=2000,
        temperature=0.7,
        stream=True
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
    collected_messages = []

    def process_response():
        for chunk in gpt_response:
            try:
                chunk_message = chunk['choices'][0]['delta']  # extract the message
                collected_messages.append(chunk_message)  # save the message
                print(chunk_message["content"], end="")
            except KeyError:
                print("Error")

    # Start a new thread to process the response
    thread = threading.Thread(target=process_response)
    thread.start()

    # Return an empty response to the client
    return '', 200