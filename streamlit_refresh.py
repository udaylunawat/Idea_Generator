import streamlit as st
st.set_page_config(layout="wide")
import os, json
from ast import literal_eval
import openai

# model_list = openai.Model.list()
# st.write(model_list)

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
    {"role": "assistant", "content": "You are an idea generator that always responds in JSON format inside a list."}
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
    additional_rule+=f"{[rules_dict]}\n\nThe response:"
    return f"{template_prompt}\n{rules_prompt}\n{additional_rule}"

def get_idea_sirji(model_name, max_tokens, temperature):
    # st.write(prompt_with_idea)
    # st.write(messages['content'], unsafe_allow_html=True)
    gpt_response =  get_gpt_response(model_name, max_tokens, temperature)
    output_text = gpt_response['choices'][0]['message']['content']
    # st.write(output_text)

    try:
        output_text = literal_eval(output_text.replace("'", "\""))
        if isinstance(output_text, list):
            output_text = output_text[0]
    except ValueError:
        pass

    finish_reason = gpt_response['choices'][0]['finish_reason']
    if finish_reason == 'length':
        st.warning("Returned output incomplete! Select fewer items!")
    elif finish_reason == 'stop':
        pass

    return output_text

models = ["gpt-3.5-turbo"]
default_model = models[0]

with open('business_structure.json', 'r') as f:
        structure = json.load(f)

st.sidebar.write('Select the items you want to include in your business model')
selected_items = st.sidebar.multiselect("Select items:", [item['name'] for item in structure], default=['Customers', 'Processes', 'Pains', 'Jobs to be Done'])
if 'idea_json' not in st.session_state:
    st.session_state.idea_json =  {item: '' for item in selected_items}

model_name = st.sidebar.selectbox('Select the OpenAI model to use:', models, index=0)
max_tokens = st.sidebar.slider('Maximum number of tokens to generate:', min_value=50, max_value=3000, value=700, help='''
The maximum number of tokens to generate in the chat completion.

The total length of input tokens and generated tokens is limited by the model's context length.''')
temperature = st.sidebar.slider('Sampling temperature:', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
# stream = st.sidebar.checkbox('Stream the output', value=False)
# st.sidebar.info("Streaming is not working currently!")
# st.sidebar.image("https://blog.udemy.com/wp-content/uploads/2013/06/bigstock-Idea-Concept-42988369.jpg")


st.title('Business Model Generator')
st.write('''Enter your business idea below and select the model and settings for the generator.
\nThen click "Generate" to create a business model structure.''', unsafe_allow_html=True)

prompt_with_rules = modify_prompt(structure, selected_items)
if len(st.session_state.chat_messages)<=1:
    st.session_state.chat_messages.append({"role": "assistant", "content": prompt_with_rules})
# TODO: Try various roles like system, assistant, user

idea = st.text_input('Enter your business idea')
generate = st.button("Generate!")
if idea:
    if generate:
        st.session_state.chat_messages.append({"role": "user", "content": f"The business idea is [{idea}]\n\n The JSON prompt:"})
        with st.spinner('Wait for it...'):
            output = get_idea_sirji(model_name, max_tokens, temperature)
            # st.write(output)
            st.session_state.idea_json = output
            st.success("Done!")
st.write(f"## Original Response")
if st.session_state.idea_json:
    # Display the information as cards with three cards per row
    columns = st.columns(3)
    for i, (key, value) in enumerate(st.session_state.idea_json.items()):
        with columns[i % 3]:
            st.write(f"## {key}")
            st.info(value)
            st.write("---")


regen_ideas = st.sidebar.multiselect("Select items to regenerate:", [item['name'] for item in structure], default=['Customers'], help="Regenrates only selected ideas! Doesn't changes existing ideas.")
if st.sidebar.button("Regenerate Ideas!"):
    if regen_ideas:
        update_message = f"Give new responses for these categories:[{regen_ideas}]\nFollow the same JSON syntax as before."
        st.session_state.chat_messages.append({"role": "user", "content": update_message})
        with st.spinner("Refreshing responses..."):
            idea_json = get_idea_sirji(model_name, max_tokens, temperature)
            # st.write(f"Idea JSON before update:{st.session_state.idea_json}")
            old_ideas = st.session_state.idea_json
            new_ideas = st.session_state.idea_json
            for k,v in idea_json.items():
                if k in new_ideas.keys():
                    new_ideas[k]=v
            st.session_state.idea_json = new_ideas
            # st.write(old_ideas, new_ideas)
            # st.write(f"Idea JSON after update:{st.session_state.idea_json}")
            # Display the information as cards with three cards per row
        try:
            st.write(f"## Refreshed Response")
            columns = st.columns(3)
            for i, (key, value) in enumerate(st.session_state.idea_json.items()):
                if key in regen_ideas:
                    with columns[i % 3]:
                        st.write(f"## {key}")
                        st.info(value)
                        st.write("---")
            st.success("Refreshed!")
        except:
            pass

if st.sidebar.checkbox("Show Raw output!"):
    c1, c2 = st.columns(2)
    with c1:
        st.write("All chat messages:",st.session_state.chat_messages)
    with c2:
        st.write("Latest Idea JSON:", st.session_state.idea_json)

st.sidebar.markdown("""## Promotion\n\n[Vivek Gupta](https://vsgupta.in/) [Dr. Nils Jeners](https://nilsjeners.de/)""", unsafe_allow_html=True)
st.sidebar.markdown("""\n[Aman Shukla](https://www.linkedin.com/in/aman-shukla-274ab2135/)  [Uday Lunawat](https://udaylunawat.github.io)""")