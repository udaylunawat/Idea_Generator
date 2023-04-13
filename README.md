# Create environment and Install dependecies

# Ideas
- [x] Allow cards to be refreshed

    - [x] append all chat history in st.session_state.chat_messages
    - [x] store usable business idea JSON in st.session_state.idea_json

- [ ] reduce tokens by giving them abbreviations

- [ ] make mind map
- [x] Deploy on Railway.io (https://ideagenerator-production.up.railway.app/)

# Installation
```bash
conda create --name openai -y
conda activate openai
pip install -r requirements.txt
```

# Run locally
```bash
streamlit run streamlit_refresh.py
```

# Roadmap

- [ ] Improve Prompts
