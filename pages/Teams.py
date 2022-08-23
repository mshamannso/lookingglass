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
    game_type_data = game_type_df.loc[teams]
    team_hero_data = team_hero_df.loc[teams]
    # replay_data = replay_data.loc[((replay_data.loc[teams]))]
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

    if not maps:
        maps = list(replay_df['MapName'].sort_values(ascending=True).unique())

    if not roles:
        roles = list(replay_df['NewRole'].sort_values(ascending=True).unique())

    if not players:
        players = list(data['Battletag'].sort_values(ascending=True).unique())

    data = data[data.Battletag.isin(players)]
    player_heroes = load_player_hero_data()
    player_heroes = player_heroes[player_heroes.Battletag.isin(players)]

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

    replay_data = replay_df.loc[teams]
    replay_data = replay_data.loc[
        (replay_data.MapName.isin(maps)) &
        (replay_data.NewRole.isin(roles)) &
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

    st.header('Team Heroes')
    team_hero_cols = ['HeroName', 'NewRole', 'Games', 'Wins', 'WinRate']
    team_hero_df = team_hero_df.reset_index()[[*team_hero_cols]]
    team_hero_df.set_index('HeroName', inplace=True)
    st.write(team_hero_df)

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
    st.write(player_heroes)

    st.header('Raw Data')
    st.write(replay_data)
