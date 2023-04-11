import streamlit as st
st.set_page_config(layout="wide")
import os, json
from ast import literal_eval
import openai

# model_list = openai.Model.list()
# st.write(model_list)

chat_message = [
  {"role": "system", "content": "You are an idea generator that always responds in JSON format."}
]
def get_gpt_response(final_prompt, model="gpt-3.5-turbo", max_tokens=300, temperature=0.7, stream=False):
    try:
        response = openai.ChatCompletion.create(
        model=model,
        messages=chat_message,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=False
        )
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None

def modify_prompt(idea, structure, selected_items):
    try:
        with open('rules.txt', 'r') as f:
            rules_prompt = f.read()
    except:
        pass
    template_prompt = f"This is the business model structure:\n"
    for item in structure:
        if item['name'] in selected_items:
            template_prompt += f"{item['name']}: {item['description']}\n"
    idea_prompt = f"The idea is [{idea}]"
    additional_rule = f"Do not include any explanations, only provide valid dictonary as response following this format without deviation.\n"
    rules_dict = {}
    for item in structure:
        if item['name'] in selected_items:
            rules_dict.update({item['name']:"content"})
    additional_rule+=f"{rules_dict}\nThe response:"
    return f"{template_prompt}\n{idea_prompt}\n{rules_prompt}\n{additional_rule}"

def get_idea_sirji(idea, structure, selected_items, model_name, temperature, stream):
    prompt_with_idea = modify_prompt(idea, structure, selected_items)
    # st.write(prompt_with_idea)
    gpt_response =  get_gpt_response(prompt_with_idea, model=model_name, temperature=temperature, stream=stream)
    st.write(gpt_response)
    output_text = gpt_response['choices'][0]['message']['content']
    finish_reason = gpt_response['choices'][0]['finish_reason']
    if finish_reason == 'length':
        st.warning("Returned output incomplete! Select fewer items!")
    elif finish_reason == 'stop':
        output_text = literal_eval(output_text.replace("'", "\""))
        return output_text

models = ["gpt-3.5-turbo"]
default_model = models[0]

with open('business_structure.json', 'r') as f:
        structure = json.load(f)

st.sidebar.write('Select the items you want to include in your business model')
selected_items = st.sidebar.multiselect("Select items:", [item['name'] for item in structure], default=['Customers', 'Processes', 'Pains', 'Jobs to be Done'])
if 'idea_json' not in st.session_state:
    st.session_state.idea_json =  [{item: '' for item in selected_items}]
model_name = st.sidebar.selectbox('Select the OpenAI model to use:', models, index=0)
max_tokens = st.sidebar.slider('Maximum number of tokens to generate:', min_value=50, max_value=3000, value=700)
temperature = st.sidebar.slider('Sampling temperature:', min_value=0.0, max_value=1.0, value=0.7, step=0.1)
stream = st.sidebar.checkbox('Stream the output', value=False)
st.sidebar.info("Streaming is not working currently!")
st.sidebar.image("https://blog.udemy.com/wp-content/uploads/2013/06/bigstock-Idea-Concept-42988369.jpg")

st.title('Business Model Generator')
st.write('Enter your business idea below and select the model and settings for the generator. Then click "Generate" to create a business model structure.')
idea = st.text_input('Enter your business idea')
generate = st.button("Generate!")
if generate:
    with st.spinner('Wait for it...'):
        st.session_state.idea_json = get_idea_sirji(idea, structure, selected_items, model_name, temperature, stream)[0]
        # info_dict
    if st.session_state.idea_json:
        st.success("Done!")
        # Display the information as cards with three cards per row
        columns = st.columns(3)
        for i, (key, value) in enumerate(st.session_state.idea_json.items()):
            with columns[i % 3]:
                st.write(f"## {key}")
                st.write(value)
                st.write("---")
st.sidebar.markdown("""## Promotion\n\n[Vivek Gupta](https://vsgupta.in/)""")
st.sidebar.markdown("""[Dr. Nils Jeners](https://nilsjeners.de/)""")
st.sidebar.markdown("""\n[Aman Shukla](https://www.linkedin.com/in/aman-shukla-274ab2135/)""")
st.sidebar.markdown("""\n[Uday Lunawat](https://udaylunawat.github.io)""")
