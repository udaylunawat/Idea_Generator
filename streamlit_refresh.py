import streamlit as st
st.set_page_config(layout="wide")
import os, json
from ast import literal_eval
import openai

# model_list = openai.Model.list()
# st.write(model_list)

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

def get_idea(model_name='gpt-3.5-turbo', max_tokens=700, temperature=0.7):
    # st.write(prompt_with_idea)
    # st.write(messages['content'], unsafe_allow_html=True)
    gpt_response =  get_gpt_response(model_name, max_tokens, temperature)
    raw_output = gpt_response['choices'][0]['message']['content']
    # st.write(raw_output)

    try:
        output_text = literal_eval(raw_output.replace("'", "\""))
        if isinstance(output_text, list):
            output_text = output_text[0]
    except ValueError:
        st.error("You have max token count way too low!")
    except SyntaxError as e:
        st.error("You have max token count way too low!")

    finish_reason = gpt_response['choices'][0]['finish_reason']
    if finish_reason == 'length':
        st.warning("Returned output incomplete! Select fewer items!")
    elif finish_reason == 'stop':
        pass

    try:
        return output_text, raw_output
    except UnboundLocalError as e:
        st.error("You have max token count way too low! Increase token count!")



def generate_new_idea(idea):
    st.session_state.chat_messages = [{"role": "assistant", "content": "You are an idea generator that always responds in JSON format inside a list."},
                                      {"role": "assistant", "content": prompt_with_rules}
                                    ]
    st.session_state.chat_messages.append({"role": "user", "content": f"The business idea is [{idea}]\n\n The JSON prompt:"})
    with loader:
        output, raw_output = get_idea(max_tokens=max_tokens)
        # st.write(output)
        st.session_state.idea_json = output
    if st.session_state.chat_messages[-1] != raw_output:
        st.session_state.chat_messages.append({"role": "assistant", "content": f"{raw_output}"})
    return output

def refresh_idea():
    update_message = f"Give new responses for these categories:[{regen_ideas}]\nFollow the same JSON syntax as before."
    st.session_state.chat_messages.append({"role": "user", "content": update_message})
    with loader:
        refresh_idea, raw_refresh = get_idea(max_tokens=max_tokens)
        if st.session_state.chat_messages[-1] != raw_refresh:
            st.session_state.chat_messages.append({"role": "assistant", "content": f"{raw_refresh}"})
        # st.write(f"Idea JSON before update:{st.session_state.idea_json}")
        old_ideas = st.session_state.idea_json
        new_ideas = refresh_idea
        for k,v in refresh_idea.items():
            if k in new_ideas.keys():
                new_ideas[k]=v
        st.session_state.idea_json = new_ideas
        # st.write(old_ideas, new_ideas)
        # st.write(f"Idea JSON after update:{st.session_state.idea_json}")
        return old_ideas, new_ideas

def show_raw():
    if st.sidebar.checkbox("Show Raw output!"):
        c1, c2 = st.columns(2)
        with c1:
            st.write("All chat messages:",st.session_state.chat_messages)
        with c2:
            st.write("Latest Idea JSON:", st.session_state.idea_json)

def show_response_cards(title, success_message):
    if all(value != '' for value in st.session_state.idea_json.values()):
        st.title(f"{title}")

        # Display the information as cards with three cards per row
        columns = st.columns(3)
        for i, (key, value) in enumerate(st.session_state.idea_json.items()):
            with columns[i % 3]:
                st.write(f"## {key}")
                st.info(value)
                st.write("---")
        st.success(success_message)


if __name__ == '__main__':
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
        {"role": "assistant", "content": "You are an idea generator that always responds in JSON format inside a list."}
        ]

    models = ["gpt-3.5-turbo"]
    default_model = models[0]

    with open('business_structure.json', 'r') as f:
            structure = json.load(f)

    ###### Sidebar elements ######
    st.sidebar.title("Select Categories 🛒")
    st.sidebar.write('Select the items you want to include in your business model')
    selected_items = st.sidebar.multiselect("Select items:", [item['name'] for item in structure], default=['Customers', 'Processes', 'Pains', 'Jobs to be Done'])
    if 'idea_json' not in st.session_state:
        st.session_state.idea_json =  {item: '' for item in selected_items}

    # model_name = st.sidebar.selectbox('Select the OpenAI model to use:', models, index=0)
    max_tokens = st.sidebar.slider('Maximum number of tokens to generate:', min_value=50, max_value=3000, value=2000, help='''
    The maximum number of tokens to generate in the chat completion.

    The total length of input tokens and generated tokens is limited by the model's context length.''')
    # temperature = st.sidebar.slider('Sampling temperature:', min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
    # stream = st.sidebar.checkbox('Stream the output', value=False)
    # st.sidebar.info("Streaming is not working currently!")
    # st.sidebar.image("https://blog.udemy.com/wp-content/uploads/2013/06/bigstock-Idea-Concept-42988369.jpg")

    ##### Main page elements ######
    st.title('Business Model Generator💡')

    prompt_with_rules = modify_prompt(structure, selected_items)
    # if len(st.session_state.chat_messages)<=1:
    #     st.session_state.chat_messages.append({"role": "assistant", "content": prompt_with_rules})
    # TODO: Try various roles like system, assistant, user

    idea = st.text_input('Enter your business idea', help='''Enter your business idea here, set options in the sidebar.
    Then click "Generate".''')

    ###### Generating new ideas ######
    generate = st.button("Generate!")
    loader = st.spinner('Wait for it...')

    if idea:
        if generate:
            _ = generate_new_idea(idea)

    if st.session_state.idea_json:
        show_response_cards("Original Response 🆕", "Done!")

    ###### Refreshing existing ideas #####
    st.sidebar.title("Refresh Ideas! ♻️")
    regen_ideas = st.sidebar.multiselect("Select items to refresh:", [item['name'] for item in structure], default=['Customers'], help="Regenerates selected ideas!")
    if st.sidebar.button("Refresh Ideas!"):
        if regen_ideas:
            old_idea, refreshed_idea = refresh_idea()
            # st.write(f"Old idea:{old_idea}\nRefreshed idea:{refreshed_idea}")
            try:
                show_response_cards("Refreshed Response ❄️", "Refreshed Ideas!")
            except:
                pass

    # show_raw()

    # st.sidebar.markdown("""## **Promotion**\n\n[Vivek Gupta](https://vsgupta.in/) [Dr. Nils Jeners](https://nilsjeners.de/)""", unsafe_allow_html=True)
    # st.sidebar.markdown("""\n[Aman Shukla](https://www.linkedin.com/in/aman-shukla-274ab2135/)  [Uday Lunawat](https://udaylunawat.github.io)""")