import json
import ollama
import requests
import streamlit as st

ollama_client = ollama.Client(host='http://ollama:11434')

package_data = {
   "name": "Reference LLM Chatbot implementation using Streamlit and Ollama",
   "version": "1.0.0-alpha.3",
}

st.set_page_config(
    page_title=package_data["name"],
    page_icon="?",
    layout="wide",
)

def initialize_chat_messages():
    st.session_state['chat_messages'] = [
        {"role": "system", "content": st.session_state['setup_prompt']}
    ]

# Initializes Streamlit session state variables
def initialize_streamlit_session():
  st.session_state['setup_prompt'] = "You're an AI assistant that helps users with a multitude of tasks."

  if 'chat_messages' not in st.session_state:
    initialize_chat_messages()

  if 'model' not in st.session_state:
    st.session_state['model'] = 'llama2'

# Loads available models from JSON file
def load_models():
    with open('./data/models.json', 'r') as file:
        data = json.load(file)
    return data['models']

# Downloads an up-to-date list of models and saves it to 'models.json'
def update_model_list():
    url = "https://ollama-models.zwz.workers.dev/"
    response = requests.get(url)
    
    if response.status_code == 200:
        models_data = response.json()
        
        # Save the models data to a file
        with open('./data/models.json', 'w') as file:
            json.dump(models_data, file)
        
        st.success("Models updated successfully.")
    else:
        st.error(f"Failed to update models. Status code: {response.status_code}")

def pull_ollama_model():
    model_name = st.session_state['model']
    response = ollama_client.pull(model=model_name, stream=True)
    
    # Initialize a placeholder for progress update
    progress_bar = st.progress(0)
    progress_status = st.empty()
    
    try:
        for progress in response:
            if 'completed' in progress and 'total' in progress:
                # Calculate the percentage of completion
                completed = progress['completed']
                total = progress['total']
                progress_percentage = int((completed / total) * 100)
                progress_bar.progress(progress_percentage)
            if 'status' in progress:
                if progress['status'] == 'success':
                    progress_status.success("Model pulled successfully!")
                    break
                elif progress['status'] == 'error':
                    progress_status.error("Error pulling the model: " + progress.get('message', 'No specific error message provided.'))
                    break
    except Exception as e:
        progress_status.error(f"Failed to pull model: {str(e)}")
    
# Model selection module to be used within the Streamlit App layout.
def sl_module_model_selection():
    st.subheader("Model")

    models = load_models()
    model_options = {model['name']: (model['name'], model['description']) for model in models}
    model_identifier = st.selectbox(
        "Choose a model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x][0]
    )

    if model_identifier:
        st.session_state['model'] = model_identifier
        
        st.write(model_options[model_identifier][1])

        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("Update list", use_container_width=True):
              update_model_list()
        with col2:
            if st.button("Pull model", use_container_width=True):
              pull_ollama_model()

def sl_module_chat():
  st.subheader("Chat")
  if st.button("Reset chat window"):
      initialize_chat_messages()

### Streamlit app
initialize_streamlit_session()

with st.sidebar:
    st.header("Preferences")
    sl_module_model_selection()
    sl_module_chat()

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