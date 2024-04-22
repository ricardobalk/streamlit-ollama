# Reference implementation for a chatbot with Streamlit and Ollama

This is a chatbot application built with Streamlit for the web interface and Ollama as the backend language model processor. In this setup, it uses Docker to containerize the application, making it easy to deploy and scale.

## Usage

**1) Start the containers**

Run the following command to start all the services defined in your Docker Compose file in detached mode:

```sh
docker compose up -d
```

**2) Pull llama2 or llama3**

Depending on the model you want to use, pull it using the following command:

```sh
docker compose exec ollama ollama pull llama2
# or
docker compose exec ollama ollama pull llama3
```

This will execute the command `ollama pull llama3` in the `ollama` container.

> Keep in mind to update `app.py` as well when you want to use `llama3` instead of `llama2`.

**3) Try it out**

Navigate to http://localhost:8501/ in your web browser to interact with the chatbot. The Streamlit interface should allow you to input text and display responses from the chatbot powered by the Ollama model.

**4) Stop the containers**

When you are done, you can stop the containers by running:

```sh
docker compose stop
```

**5) Remove the containers and volumes (optional)**

To completely remove all containers and clean up volumes created by Docker Compose, use:

```sh
docker compose down -v
```