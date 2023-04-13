# Create environment and Install dependecies

# Ideas
- [x] Allow cards to be refreshed

    - [x] append all chat history in st.session_state.chat_messages
    - [x] store usable business idea JSON in st.session_state.idea_json

- [ ] reduce tokens by giving them abbreviations

- [ ] make mind map
- [x] Deploy on Railway.io

# Installation
```bash
conda create --name openai -y
conda activate openai
pip install -r requirements.txt
```

# Run locally
```bash
streamlit run streamlit_card_refresh.py
```

# Roadmap

- [ ] Improve Prompts
