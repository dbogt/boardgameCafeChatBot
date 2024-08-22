import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
import openai
from pathlib import Path
from nltk.corpus import stopwords

#Based off tutorial from: https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/
#Great repo: https://github.com/carolinedfrasca/llamaindex-chat-with-streamlit-docs/blob/main/streamlit_app.py

st.set_page_config(page_title="Chat with Board Game Cafe Bot, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
# openai.api_key = st.secrets.openai_key
adminPass = st.secrets.adminPass

appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Feb 8, 2024 \n
Purpose: Showcase OpenAI API and Llamaindex to create a chatbot \n
This chatbot is for a ficticious board game cafe that recommends to customers what games to play given preference on game theme, party/group size and time available to play a game. 
I first created and tested the bot in a Google Colab file and trained it with a CSV of my game collection. I then used llamaindex package to create a vector index of the data (so that openAI API has an easier time parsing the data). 
The code behind can be found on my github: https://github.com/dbogt/boardgameCafeChatBot.

From the left sidebar menu choose one of the pages:
1. app - This is the main chatbot. Once you enter your own OpenAI API Key, it will allow you to try the bot.
You will have two options: 
- concise model - model trained with a temperature setting of 0.5 on gpt-3.5-turbo and chat mode of "condense_question"
- openai friendly model -  model trained with a temperature setting of 1 on gpt-3.5-turbo and chat mode of "openai"
As you play around with the models, you will notice the openai frindly model will provide longer answers with a friendlier tone.

2. Explore Data Set - This page allows the user to explore the cafe's board game collection that was used to train the bot and "check" the answers the bot is giving. As you experiment with the bot, you will notice a couple things:
- The friendly model has a higher tendancy to "hallucinate" and provide recommendations for games that are not in the cafe/collection or games with faulty information.
- Both models also bring in "external" information about the games it is recommending. 
- For example, the csv used to train the data only had tags for some of the games on themes, but no descriptions of the game. 
- Yet, the models are able to provide accurate descriptions of the games due to the original gpt being trained on board games data sets.
"""
with st.expander("See app info"):
    st.write(appDetails)

st.title("Chat with Board Game Cafe Bot, powered by LlamaIndex 💬🦙")
st.info("This app was inspired by the tutorial from [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about board game recommendations at our cafe! Please provide how many people are in your group and if you have any time constraints."}
    ]


sys_prompt = """You are a chatbot for a board game cafe, equipped to help customers select the perfect game from the cafe's collection based on their preferences, group size, and available playtime. \
 Your interactions begin by inquiring about the number of participants, the duration they have for game play, and their preferred game genre. \
 Utilize the information provided in the csv file to identify games that match their criteria, ensuring the selected game accommodates the group's size (within the minPlayers and maxPlayers range) and fits within their time frame by checking the playingTime column. \
 If the customer provides a time in minutes, find a game with play time that does not exceed the provided time. \
 Use the userComment field in the file to identify games that match the customer's preferred game genre. For example, if the user provides "Space" as a theme, find any games that contain the word "Space" in the userComment column. \
 If the user asks about most popular games, or most played games, look at the "numPlays" columns and find any games with more than 50 plays. \
 If the user asks for new or old games look at the "yearPublished" column and recommend games that have come out in the last 3 years for new and games that are older than 20 years for old games. \
 Your recommendations should be inventive yet accurate, exclusively suggesting games listed in the provided file, without fabricating non-existent options.
 """

sys_prompt2 = """You are a chatbot for a board game cafe, equipped to help customers select the perfect game from the cafe's collection based on their preferences, group size, and available playtime. \
 Your interactions begin by inquiring about the number of participants, the duration they have for game play, and their preferred game genre. \
 Utilize the information provided in the csv file to identify games that match their criteria, ensuring the selected game accommodates the group's size (within the minPlayers and maxPlayers range) and fits within their time frame (playingTime). \
 If the customer provides a time in minutes, find a game with play time that does not exceed the provided time. \
 Use the userComment field in the file to identify games that match the customer's preferred game genre. For example, if the user provides "Space" as a theme, find any games that contain the word "Space" in the userComment column. \
 If the user asks about most popular games, or most played games, look at the "numPlays" columns and find any games with more than 50 plays. \
 If the user asks for new or old games look at the "yearPublished" column and recommend games that have come out in the last 3 years for new and games that are older than 20 years for old games. \
 Your recommendations should be inventive. Try to suggest games listed in the provided file, without fabricating non-existent options. \
 Use a friendly and humorous tone, with some hints of Canadianisms.
 """


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the board games collection csv file – hang tight! This should take 1-2 minutes."):
        
      #SimpleCSVReader = download_loader("SimpleCSVReader")
      #loader = SimpleCSVReader(encoding="utf-8")
      #docs = loader.load_data(file=Path('boardgames.csv'))
      reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
      docs = reader.load_data()
    #   service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=sys_prompt))
    #   index = VectorStoreIndex.from_documents(docs, service_context=service_context)
      
      Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.5,
            system_prompt=sys_prompt) 
      
      index = VectorStoreIndex.from_documents(docs)
      return index

@st.cache_resource(show_spinner=False)
def load_data2():
    with st.spinner(text="Loading and indexing the board games collection csv file – hang tight! This should take 1-2 minutes."):
        
      #SimpleCSVReader = download_loader("SimpleCSVReader")
      #loader = SimpleCSVReader(encoding="utf-8")
      #docs = loader.load_data(file=Path('boardgames.csv'))
      reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
      docs = reader.load_data()
      Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=1,
            system_prompt=sys_prompt2) 
      
      index = VectorStoreIndex.from_documents(docs)
      return index

#Enter open AI Key
keyOK = 0
openai_api_key = st.sidebar.text_input('OpenAI API Key', type="password")
if openai_api_key == adminPass:
         openai.api_key = st.secrets.openai_key
         keyOK = 1
else:
         if not openai_api_key.startswith('sk-'):
             keyOK = 0
             openai.api_key = ""
             st.sidebar.warning('Please enter your OpenAI API key!', icon='⚠')
         
         else:
             keyOK = 1
             openai.api_key = openai_api_key    
         
if keyOK:
         index = load_data()
         index2 = load_data2()
         
         if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
                 st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
         
         if "chat_engine2" not in st.session_state.keys(): # Initialize the chat engine
                 st.session_state.chat_engine2 = index2.as_chat_engine(chat_mode="openai", verbose=True)
         
         if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
             st.session_state.messages.append({"role": "user", "content": prompt})
         
         for message in st.session_state.messages: # Display the prior chat messages
             with st.chat_message(message["role"]):
                 st.write(message["content"])
else:
         st.warning('Please enter your OpenAI API key!', icon='⚠')
         
if keyOK:
         modelPicks = ['concise model', 'openai friendly model']
         model = st.sidebar.selectbox('Pick a chatbot model',modelPicks)

         # If last message is not from assistant, generate a new response
         if st.session_state.messages[-1]["role"] != "assistant":
             with st.chat_message("assistant"):
                 with st.spinner("Thinking..."):
         
                     if model == "concise model":
                              response = st.session_state.chat_engine.chat(prompt)
                     else:
                              response = st.session_state.chat_engine2.chat(prompt)
                     st.write(response.response)
                     message = {"role": "assistant", "content": response.response}
                     st.session_state.messages.append(message) # Add response to message history

         
del openai_api_key #delete key from session state after every run

# Download chat history
if keyOK:
         text = str(st.session_state.messages)
         import pandas as pd
         chatDF = pd.DataFrame(st.session_state.messages)
         st.sidebar.download_button('Download Chat History as TXT', str(text), file_name="chat.txt")
         st.sidebar.download_button('Download Chat History as CSV', data=chatDF.to_csv(index=False).encode('utf-8'), file_name="chat.csv")

         


