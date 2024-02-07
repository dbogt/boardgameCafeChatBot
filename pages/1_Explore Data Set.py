import pandas as pd
import streamlit as st

df = pd.read_csv('boardgames.csv')
st.title("Board Game Collection")
st.write("Filter for games on the side")

gamesSearch = st.sidebar.multiselect('What game are you looking for?',df['name'])
gameFilter = "|".join(gamesSearch)

df = df[df['name'].str.contains(gameFilter, regex=True)]

#Filter for time taken
timeFilter = st.sidebar.checkbox("Filter for playing time")
if timeFilter:
    timeMin, timeMax = st.sidebar.slider("Playing time (minutes)",0,int(df['playingTime'].max()),(0,120))
    df = df[(df['playingTime']>=timeMin) & (df['playingTime']<=timeMax)]
else:
    df = df.copy()

#Filter for num of players
numPlFilter = st.sidebar.checkbox("Filter for # of players")
if numPlFilter:
    minPl, maxPl = st.sidebar.slider('Select number of players', 1, 12, (2, 4))
    df = df[(df['maxPlayers']>=maxPl) & (df['minPlayers']<=minPl)]
else:    
    df = df.copy()

st.write(df)
