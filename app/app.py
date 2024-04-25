import datetime
import json
import ollama
import streamlit as st

ollama_client = ollama.Client(host='http://ollama:11434')
         
package_data = {
   "name": "Reference LLM Chatbot implementation using Streamlit and Ollama",
   "version": "1.0.0-alpha.1",
}

st.set_page_config(
    page_title=package_data["name"],
    page_icon="?",
    layout="wide",
)

# Initializes Streamlit session state variables
def initialize_streamlit_session():
  if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "system", "content": "You're an AI assistant that helps users with a multitude of tasks."}
    ]

  if 'model' not in st.session_state:
    st.session_state['model'] = 'llama2'

# Loads available models from JSON file
def load_models():
    with open('./data/models.json', 'r') as file:
        data = json.load(file)
    return data['models']

# Model selection module to be used within the Streamlit App layout.
def sl_module_model_selection():
    st.subheader("Model")
    models = load_models()
    # Creating a dropdown box with names and descriptions stored separately
    model_options = {model['id']: (model['name'], model['description']) for model in models}
    model_id = st.selectbox(
        "Choose a model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x][0]  # Display only model names in the dropdown
    )
    if model_id:
        st.session_state['model'] = model_id
        st.write(model_options[model_id][1]) # Accessing the description of the model


### Streamlit app

initialize_streamlit_session()

with st.sidebar:
    st.header("Preferences")
    sl_module_model_selection()

st.header(f"{package_data['name']}")

for message in st.session_state['chat_messages']:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("How can I help?"):
  st.session_state['chat_messages'].append({"role": "user", "content": prompt})

  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    response_placeholder = st.empty()
    full_response = ""
    for chunk in ollama_client.chat(
        model=st.session_state['model'],
        messages=st.session_state['chat_messages'],
        stream=True,
    ):
      full_response += chunk['message']['content']
      response_placeholder.markdown(full_response + "▌")
    response_placeholder.markdown(full_response)

  st.session_state.chat_messages.append({"role": "assistant", "content": full_response})