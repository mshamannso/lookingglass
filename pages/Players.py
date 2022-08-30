import datetime

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
from datetime import datetime

st.set_page_config(page_title="Player Data", page_icon="📊")

st.markdown("# Player Totals")
st.sidebar.header("Player Totals")


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


@st.cache
def load_team_hero_data() -> pd.DataFrame:
    path = './data/TeamHeroTotal.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame


@st.cache
def load_player_hero_data() -> pd.DataFrame:
    path = './data/TeamMemberHeroTotal.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame


df = load_data()
# game_type_df = load_game_type_data()
# replay_df = load_replay_data()
team_hero_df = load_team_hero_data()
players = st.sidebar.selectbox(
    "Choose players", list(df['Battletag'].sort_values(ascending=True).unique())
)

if not players:
    st.error("Please select at least one team.")
else:
    player_heroes = load_player_hero_data()
    roles = st.sidebar.multiselect(
        "Choose roles", list(player_heroes['NewRole'].sort_values(ascending=True).unique())
    )

    heroes = st.sidebar.multiselect(
        "Choose heroes", list(player_heroes['HeroName'].sort_values(ascending=True).unique())
    )

    if not roles:
        roles = list(player_heroes['NewRole'].sort_values(ascending=True).unique())

    if not heroes:
        heroes = list(player_heroes['HeroName'].sort_values(ascending=True).unique())

    data = df[df.Battletag.str.lower().isin([players])]

    data.reset_index(inplace=True)
    col1, col2, col3, col4 = st.columns(4)

    input_col1, input_col2, input_col3 = st.columns(3)
    min_games = input_col1.number_input('Select a min number of games played', min_value=0, value=5)

    st.info('You can use ctrl+f to search the tables.')

    player_heroes = player_heroes.loc[
        (player_heroes.NewRole.isin(roles)) &
        (player_heroes.HeroName.isin(heroes)) &
        (player_heroes.Battletag.str.lower().isin([players]))
        ]

    st.header('Player Heroes')

    player_cols = [
        'Battletag'
        , 'HeroName'
        , 'NewRole'
    ]
    player_metrics = [
        'Total'
        , 'TotalWins'
        , 'TotalLosses'
        , 'HeroWinRate'
        , 'IsWinner'
        , 'Kills'
        , 'Assists'
        , 'Deaths'
        , 'ExperienceContribution'
        , 'FirstToTen'
        , 'Level'
        , 'HeroDamage'
        , 'Healing'
        , 'Takedowns'
        , 'SelfHealing'
        , 'DamageTaken'
        , 'TimeSpentDead'
    ]

    player_cols = player_cols + player_metrics
    player_heroes = player_heroes.reset_index()[[*player_cols]]
    player_heroes.set_index('Battletag', inplace=True)
    x_df = player_heroes[player_heroes.Total >= min_games].sort_values('Total', ascending=False)

    hero_chart = (
        alt.Chart(x_df.reset_index())
        .mark_bar(opacity=0.7, size=15)
        .encode(
            x="Total:Q",
            y=alt.Y("HeroName:N"),
            color="Battletag:N",
            tooltip=[*player_cols]
        )
    )
    st.altair_chart(hero_chart, use_container_width=True)

    st.dataframe(x_df)