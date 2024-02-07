import pandas as pd
import streamlit as st

df = pd.read_csv('boardgames_full.csv')
st.set_page_config(layout="wide",page_title='Board Game Cafe Collection')
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

st.data_editor(
    df,
    column_config={
        "image": st.column_config.ImageColumn(
            "Image", help="Preview board game covers"
        ),
        "playingTime": st.column_config.ProgressColumn(
            "Playing Time",
            help="Playing Time in minutes",
            format="%f",
            min_value=0,
            max_value=120,
        ),
         "averageRating": st.column_config.ProgressColumn(
            "Average Rating",
            help="Avg Rating from BGG",
            format="%f",
            min_value=0,
            max_value=10,
        ),
             "numPlays": st.column_config.ProgressColumn(
            "Number of Plays",
            help="Number of plays logged at cafe",
            format="%f",
            min_value=0,
            max_value=300,
        ),
    },
    hide_index=True,
)
