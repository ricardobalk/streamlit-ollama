import datetime
import streamlit as st
import ollama

ollama_client = ollama.Client(host='http://ollama:11434')
         
package_data = {
   "name": "Reference LLM Chatbot implementation using Streanlit and Ollama",
   "version": "1.0.0-alpha.1",
   "release_date": datetime.date(2024, 4, 22),
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

footer_text = f"{package_data['name']} {package_data['version']}, geupdate op {package_data['release_date'].strftime('%B %d, %Y')}."

with st.container():
  st.header(f"{package_data['name']} ({package_data['release_date'].strftime('%d %B %Y')})")
  # st.write(footer_text)

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
          model='llama2',
          stream=True,
          messages=st.session_state['chat_messages'],
      ):
        full_response += chunk['message']['content']
        response_placeholder.markdown(full_response + "▌")
      response_placeholder.markdown(full_response)

    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})