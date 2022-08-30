import datetime

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
from datetime import datetime

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
game_type_df = load_game_type_data()
replay_df = load_replay_data()
team_hero_df = load_team_hero_data()
teams = st.sidebar.selectbox(
    "Choose teams", list(df.index.unique().sort_values(ascending=True))
)

if not teams:
    st.error("Please select at least one team.")
else:
    map_col, role_col, player_col = st.columns(3)
    data = df.loc[teams]
    maps = st.sidebar.multiselect(
        "Choose maps", list(replay_df['MapName'].sort_values(ascending=True).unique())
    )

    roles = st.sidebar.multiselect(
        "Choose roles", list(replay_df['NewRole'].sort_values(ascending=True).unique())
    )

    players = st.sidebar.multiselect(
        "Choose players", list(data['Battletag'].sort_values(ascending=True).unique())
    )

    heroes = st.sidebar.multiselect(
        "Choose heroes", list(replay_df['HeroName'].sort_values(ascending=True).unique())
    )

    game_type_data = game_type_df.loc[teams]
    team_hero_data = team_hero_df.loc[teams]

    if not maps:
        maps = list(replay_df['MapName'].sort_values(ascending=True).unique())

    if not roles:
        roles = list(replay_df['NewRole'].sort_values(ascending=True).unique())

    if not players:
        players = list(data['Battletag'].sort_values(ascending=True).unique())

    if not heroes:
        heroes = list(replay_df['HeroName'].sort_values(ascending=True).unique())

    data = data[data.Battletag.str.lower().isin(players)]

    replay_cols = [
        'TeamName'
        , 'Battletag'
        , 'MapName'
        , 'GameType'
        , 'HeroName'
        , 'NewRole'
        , 'GameDate'
        , 'IsWinner'
        , 'FirstToTen'
        , 'Kills'
        , 'Assists'
        , 'Takedowns'
        , 'Deaths'
        , 'Level'
        , 'HeroDamage'
        , 'SiegeDamage'
        , 'Healing'
        , 'SelfHealing'
        , 'DamageTaken'
        , 'ExperienceContribution'
        , 'HighestKillStreak'
        , 'TownKills'
        , 'Multikill'
        , 'TimeSpentDead'
        , 'MercCampCaptures'
        , 'WatchTowerCaptures'
        , 'MetaExperience'
        , 'ClutchHeals'
        , 'Escapes'
        , 'Vengeance'
        , 'OutnumberedDeaths'
        , 'TeamfightEscapes'
        , 'TeamfightHealing'
        , 'TeamfightDamageTaken'
        , 'TeamfightHeroDamage'
        , 'PhysicalDamage'
        , 'SpellDamage'
        , 'RegenGlobes'
    ]

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
    col1, col2, col3, col4 = st.columns(4)

    total_games = game_type_data['Games'].sum()
    win_rate = (round((game_type_data['Wins'].sum() / total_games) * 100, 2))
    avg_account_level = int(round(data[['TeamName', 'AccountLevel']].mean()['AccountLevel'], 0))

    first_played_together = datetime.strptime(data['FirstPlayed'][0], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
    last_played_together = datetime.strptime(data['LastPlayed'][0], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')

    col1.metric("Total Players", len(data))
    col1.metric("Total Games", total_games)
    col2.metric("Avg Account Level", avg_account_level)
    col2.metric("Win Rate", win_rate)
    col3.metric("Avg Team Rank", data[['TeamName', 'TeamRank']].max()['TeamRank'])
    col4.metric('First Played Together (utc)', first_played_together)
    col4.metric('Last Played Together (utc)', last_played_together)

    replay_data = replay_df.loc[teams]
    replay_data = replay_data.loc[
        (replay_data.MapName.isin(maps)) &
        (replay_data.NewRole.isin(roles)) &
        (replay_data.HeroName.isin(heroes)) &
        (replay_data.Battletag.str.lower().isin(players))
        ]
    replay_data = replay_data.reset_index()[[*replay_cols]]
    replay_data.set_index('TeamName', inplace=True)

    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.7, size=15)
        .encode(
            x="Battletag:N",
            y=alt.Y("GamesPlayed:Q", stack=None),
            color="TeamName:N",
            tooltip=cols
        )
    )
    st.altair_chart(chart, use_container_width=True)

    input_col1, input_col2, input_col3 = st.columns(3)
    min_games = input_col1.number_input('Select a min number of games played', min_value=0, value=5)

    st.header('Team Heroes')
    st.info('You can use ctrl+f to search the tables.')
    team_hero_cols = ['HeroName', 'NewRole', 'Games', 'Wins', 'WinRate']
    team_hero_df = team_hero_df.loc[teams]
    team_hero_df = team_hero_df.loc[
        (team_hero_df.NewRole.isin(roles)) &
        (team_hero_df.HeroName.isin(heroes))
        ]

    player_heroes = load_player_hero_data()
    player_heroes = player_heroes.loc[
        (player_heroes.NewRole.isin(roles)) &
        (player_heroes.HeroName.isin(heroes)) &
        (player_heroes.Battletag.str.lower().isin(players))
        ]

    team_hero_df = team_hero_df.reset_index()[[*team_hero_cols]]

    team_player_hero_df = replay_data.groupby(['HeroName', 'NewRole', 'Battletag']).agg(
       PlayerGames=('Battletag', 'count')
        , PlayerWins=('IsWinner', 'sum')
    ).reset_index()
    team_player_hero_piv = team_player_hero_df.pivot_table(
        index=['HeroName', 'NewRole']
        , columns=['Battletag']
        , values=['PlayerGames']
        , fill_value=0
    )

    team_player_hero_piv.columns = team_player_hero_piv.columns.droplevel(0)
    team_player_hero_piv = team_player_hero_piv.reset_index()
    team_hero_df = pd.merge(team_hero_df, team_player_hero_piv, left_on=['HeroName', 'NewRole'], right_on=['HeroName', 'NewRole'])
    team_hero_df.set_index('HeroName', inplace=True)
    team_hero_df = team_hero_df[team_hero_df.Games >= min_games].sort_values('Games', ascending=False)
    st.dataframe(team_hero_df.style.highlight_max(
        subset=['Games', 'Wins'], axis=0, color='green'
    ), width=1000)
    team_player_hero_df = team_player_hero_df.reset_index()
    hero_chart = (
        alt.Chart(team_player_hero_df[team_player_hero_df.PlayerGames >= min_games])
        .mark_bar(opacity=0.7, size=15)
        .encode(
            x="PlayerGames:Q",
            y=alt.Y("HeroName:N"),
            color="Battletag:N"
        )
    )
    st.altair_chart(hero_chart, use_container_width=True)

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
    st.dataframe(player_heroes[player_heroes.Total >= min_games].sort_values('Total', ascending=False))

    st.header('Raw Data')
    st.dataframe(replay_data)
