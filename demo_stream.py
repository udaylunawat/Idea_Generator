import os
import streamlit as st
import openai
import json
from ast import literal_eval

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up default configuration for OpenAI chat completion
model = "gpt-3.5-turbo"
max_tokens = 50
temperature = 0.5

# Initialize Streamlit page layout
st.set_page_config(page_title="OpenAI Chat Demo", page_icon=":speech_balloon:")

st.markdown("""
    <style>
        .card-deck {
            margin-bottom: 20px;
        }
        .card {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 0.25rem;
            padding: 1rem;
        }
        .card-title {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)
# Define function to get OpenAI chat response
# @st.cache(allow_output_mutation=True, show_spinner=False)
def get_chat_response(idea):
    try:
        # Create chat completion request
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": """You are an idea generator that always responds in JSON format inside a list."""},
                {"role": "user", "content": f"The business idea is [{idea}]\n\n The JSON prompt:"}],
            max_tokens=193,
            temperature=0,
            stream=True,
        )

        json_string = ''
        for index, i in enumerate(response):
            if "content" in i.choices[0].delta:
                content = i.choices[0].delta.content
                yield content

    except TypeError as e:
        st.write(e)
    except KeyError as e:
        st.write(e)
    except AttributeError as e:
        st.write(e)


# Define Streamlit app
def app():
    # Set up Streamlit page layout
    st.title("OpenAI Chat Demo")
    st.write("Type your prompt below and watch the chat response appear in real time!")
    st.write("Press the Stop button to end the chat.")
    st.write("---")

    # Get user prompt
    prompt = st.text_input("User Prompt")
    generate = st.button("Generate")

    # Set up streamlit components for chat response display
    chat_responses = st.empty()
    stop = st.button("Stop", key="stop")

    def get_key_value(buffer, item_count):
        dict_start, value_end = None, None
        title, value = None, None
        # print(buffer)
        try:
            dict_start = buffer.find("[{")
            seperator = buffer.find(":")
            value_end = buffer.index("\",")
            title = buffer[dict_start+3:seperator][:-1].replace('"', '').replace("{", "")
            value = buffer[seperator+2:value_end].strip('"').strip('\'')
        except:
            pass
        if title and value:
            item_count += 1
            # print(item_count)
            return item_count, title, value, ""
        return item_count, None, None, buffer

    # Start chat response generator
    if generate:
        buffer = ""
        item_count = 0
        gpt_stream = get_chat_response(prompt)

        # Set up columns for display
        col1, col2, col3 = st.columns(3)

        for index, json_chunk in enumerate(gpt_stream):
            buffer += json_chunk
            item_count, title, value, buffer = get_key_value(buffer, item_count)

            # Display title and value in columns
            if title and value:
                if item_count % 3 == 1:
                    with col1:
                        st.title(title)
                        st.info(value)
                elif item_count % 3 == 2:
                    with col2:
                        st.title(title)
                        st.info(value)
                else:
                    with col3:
                        st.title(title)
                        st.info(value)


# Run Streamlit app
if __name__ == "__main__":
    app()