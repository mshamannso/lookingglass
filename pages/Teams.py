import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Team Data", page_icon="📊")

st.markdown("# Team Totals")
st.sidebar.header("Team Totals")


@st.cache
def load_data() -> pd.DataFrame:
    path = './data/TeamRollup.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame

@st.cache
def load_game_type_data() -> pd.DataFrame:
    path = './data/TeamGameTypeTotal.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame

@st.cache
def load_replay_data() -> pd.DataFrame:
    path = './data/TeamReplayData.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame


df = load_data()
game_type_df = load_game_type_data()
replay_df = load_replay_data()
teams = st.selectbox(
    "Choose teams", list(df.index.unique().sort_values(ascending=True))
)

if not teams:
    st.error("Please select at least one team.")
else:
    data = df.loc[teams]
    game_type_data = game_type_df.loc[teams]
    replay_data = replay_df.loc[teams]
    cols = [
        'TeamName'
        , 'TeamRank'
        , 'Battletag'
        , 'AccountLevel'
        , 'Rank'
        , 'SL_MMR'
        , 'LastNinety'
        , 'GamesPlayed'
        , 'Bruiser'
        , 'Healer'
        , 'Support'
        , 'Tank'
        , 'DPS'
    ]
    data.reset_index(inplace=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players", len(data))
    col1.metric("Total Games", game_type_data['Games'].sum())
    col2.metric("Avg Account Level", int(round(data[['TeamName', 'AccountLevel']].mean()['AccountLevel'], 0)))
    col3.metric("Avg Team Rank", data[['TeamName', 'TeamRank']].max()['TeamRank'])
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.7)
        .encode(
            x="Battletag:N",
            y=alt.Y("GamesPlayed:Q", stack=None),
            color="TeamName:N",
            tooltip=cols
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # st.write(game_type_data[game_type_data.GameType == 'Custom']['Games'])

    st.header("Maps")

    st.header("Heroes")

    st.header("Players")
    # st.write(replay_data.sort_index())

    st.header("Replay Data")
    st.write(replay_data.sort_index())
