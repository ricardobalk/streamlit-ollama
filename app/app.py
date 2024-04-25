import datetime
import streamlit as st
import ollama

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

# Initialise the chat if not in Streamlit session's state.
if 'chat_messages' not in st.session_state:
  st.session_state['chat_messages'] = [
      {"role": "system", "content": "You're an AI assistant that helps users with a multitude of tasks."}
  ]

if 'model' not in st.session_state:
  st.session_state['model'] = 'llama2'

with st.sidebar:
  st.header("Preferences")

  st.subheader("Model")
  model = st.radio(
    "Choose a model",
    ("llama2", "llama3")
  )
  if model:
    st.session_state['model'] = model

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