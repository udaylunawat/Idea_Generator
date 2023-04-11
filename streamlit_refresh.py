import streamlit as st
st.set_page_config(layout="wide")
import os, json
from ast import literal_eval
import openai

# model_list = openai.Model.list()
# st.write(model_list)

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
    {"role": "system", "content": "You are an idea generator that always responds in JSON format."}
    ]



def get_gpt_response(model="gpt-3.5-turbo", max_tokens=300, temperature=0.7, stream=False):
    try:
        response = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state.chat_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=False
        )
        return response

    except Exception as e:
        st.write(f"Error: {e}")
        return None

def modify_prompt(structure, selected_items):
    try:
        with open('rules.txt', 'r') as f:
            rules_prompt = f.read()
    except:
        pass
    template_prompt = f"This is the business model structure:\n\n'''\n"
    for item in structure:
        if item['name'] in selected_items:
            template_prompt += f"\n{item['name']}: {item['description']}\n"
    template_prompt+="\n'''\n"
    additional_rule = f"Do not include any explanations, only provide valid dictonary as response following this format without deviation.\n"
    rules_dict = {}
    for item in structure:
        if item['name'] in selected_items:
            rules_dict.update({item['name']:"content"})
    additional_rule+=f"{rules_dict}\n\nThe response:"
    return f"{template_prompt}\n{rules_prompt}\n{additional_rule}"

# def update_card(card_name, updated_info):
#     st.session_state.idea_json[card_name] = updated_info

def get_idea_sirji(prompt_with_idea, model, max_tokens, temperature):
    st.write(st.session_state.chat_messages)
    # st.write(prompt_with_idea)
    # st.write(messages['content'], unsafe_allow_html=True)
    gpt_response =  get_gpt_response(idea_prompt = f"\nHere's the idea [{idea}]\nThe Prompt is:")
    st.write(gpt_response['choices'][0]['message'])
    output_text = gpt_response['choices'][0]['message']['content']
    finish_reason = gpt_response['choices'][0]['finish_reason']
    if finish_reason == 'length':
        st.warning("Returned output incomplete! Select fewer items!")
    elif finish_reason == 'stop':
        output_text = literal_eval(output_text.replace("'", "\""))
        return output_text[0]

def print_json_columns():
    columns = st.columns(3)
    for i, (key, value) in enumerate(st.session_state.idea_json.items()):
        with columns[i % 3]:
            st.write(f"## {key}")
            st.write(value)
            st.write("---")

models = ["gpt-3.5-turbo"]
default_model = models[0]

with open('business_structure.json', 'r') as f:
        structure = json.load(f)

st.sidebar.write('Select the items you want to include in your business model')
selected_items = st.sidebar.multiselect("Select items:", [item['name'] for item in structure], default=['Customers', 'Processes', 'Pains', 'Jobs to be Done'])
if 'idea_json' not in st.session_state:
    st.session_state.idea_json =  [{item: '' for item in selected_items}]

# st.write(st.session_state.idea_json)
model_name = st.sidebar.selectbox('Select the OpenAI model to use:', models, index=0)
max_tokens = st.sidebar.slider('Maximum number of tokens to generate:', min_value=50, max_value=3000, value=700, help='''
The maximum number of tokens to generate in the chat completion.

The total length of input tokens and generated tokens is limited by the model's context length.''')
temperature = st.sidebar.slider('Sampling temperature:', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
stream = st.sidebar.checkbox('Stream the output', value=False)
# st.sidebar.info("Streaming is not working currently!")
# st.sidebar.image("https://blog.udemy.com/wp-content/uploads/2013/06/bigstock-Idea-Concept-42988369.jpg")


st.title('Business Model Generator')
st.write('''Enter your business idea below and select the model and settings for the generator.
\nThen click "Generate" to create a business model structure.''', unsafe_allow_html=True)
idea = st.text_input('Enter your business idea')
prompt_with_idea = modify_prompt(idea, structure, selected_items)
# TODO: Try various roles like system, assistant, user
st.session_state.chat_messages.append({"role": "user", "content": prompt_with_idea})

generate = st.button("Generate!")
if generate:
    with st.spinner('Wait for it...'):
        st.session_state.idea_json = get_idea_sirji(prompt_with_idea, structure, selected_items, default_model, temperature, stream)
        # info_dict
    if st.session_state.idea_json:
        st.success("Done!")
        # Display the information as cards with three cards per row
        print_json_columns()

regen_ideas = st.sidebar.multiselect("Select items to regenerate:", [item['name'] for item in structure], default=[], help="Regenrates only selected ideas! Doesn't changes existing ideas.")
if st.sidebar.button("Regenerate Ideas!"):
    if regen_ideas:
        update_message = f"Give new responses for these categories:[{regen_ideas}]\nFollow the same JSON syntax as before."
        st.session_state.chat_messages.append({"role": "user", "content": update_message})
        idea_json = get_idea_sirji(idea, structure, selected_items, default_model, temperature, stream)
        for i,v in idea_json.values():
            st.write(i,v)
        print_json_columns()


    # if st.session_state.idea_json:
    #     st.success("Done!")
    #     # Display the information as cards with three cards per row
    #     columns = st.columns(3)
    #     for i, (key, value) in enumerate(st.session_state.idea_json.items()):
    #         with columns[i % 3]:
    #             st.write(f"## {key}")
    #             st.write(value)
    #             st.write("---")


st.sidebar.markdown("""## Promotion\n\n[Vivek Gupta](https://vsgupta.in/) [Dr. Nils Jeners](https://nilsjeners.de/)""", unsafe_allow_html=True)
st.sidebar.markdown("""\n[Aman Shukla](https://www.linkedin.com/in/aman-shukla-274ab2135/)  [Uday Lunawat](https://udaylunawat.github.io)""")
