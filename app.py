import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from pathlib import Path
from llama_index import download_loader

#Based off tutorial from: https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/

st.set_page_config(page_title="Chat with Board Game Cafe Bot, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Chat with Board Game Cafe Bot, powered by LlamaIndex 💬🦙")
st.info("This app was inspired by the tutorial from [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about board game recommendations at our cafe!"}
    ]


sys_prompt = """You are a chatbot for a board game cafe, equipped to help customers select the perfect game from the cafe's collection based on their preferences, group size, and available playtime. \
 Your interactions begin by inquiring about the number of participants, the duration they have for game play, and their preferred game genre. \
 Utilize the information provided in the csv file to identify games that match their criteria, ensuring the selected game accommodates the group's size (within the minPlayers and maxPlayers range) and fits within their time frame (playingTime). \
 Use the userComment field in the file to identify games that match the customer's preferred game genre. \
 Your recommendations should be inventive yet accurate, exclusively suggesting games listed in the provided file, without fabricating non-existent options.
 """

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the board games collection csv file – hang tight! This should take 1-2 minutes."):
      SimpleCSVReader = download_loader("SimpleCSVReader")
      loader = SimpleCSVReader(encoding="utf-8")
      docs = loader.load_data(file=Path('boardgames.csv'))
      service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=sys_prompt))
      index = VectorStoreIndex.from_documents(docs, service_context=service_context)
      return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history