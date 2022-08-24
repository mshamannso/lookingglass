import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Hero Data", page_icon="📊")

st.markdown("# Hero Totals")
st.sidebar.header("Hero Totals")

@st.cache
def load_data() -> pd.DataFrame:
    path = './data/hero_stats.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('HeroName', inplace=True)
    return data_frame


heroes_df = load_data()
st.header('Heroes Stats')

left_team = st.sidebar.multiselect(
    "Left Team", list(heroes_df.index.unique().sort_values(ascending=True).unique())
)

right_team = st.sidebar.multiselect(
    "Right Team", list(heroes_df.index.unique().sort_values(ascending=True).unique())
)


if not [*left_team, *right_team]:
    heroes = list(heroes_df.index.unique().sort_values(ascending=True).unique())
else:
    heroes = [*left_team, *right_team]

heroes_data = heroes_df.loc[heroes].drop_duplicates()

categories = [
    'HeroName'
, 'WaveClear'
, 'Engage'
, 'Peel'
, 'TeamSustain'
, 'SelfSustain'
, 'SoloLane'
, 'Fight'
, 'Macro'
, 'Artillery'
, 'Protect'
, 'Pick'
]

comp_types = [
'Fight'
, 'Macro'
, 'Artillery'
, 'Protect'
, 'Pick'
]

ct = st.container()
if len(heroes) > 10:
    st.error("Only ten heroes can be in in a draft.")
else:

    left_team_data = heroes_df.loc[left_team]
    right_team_data = heroes_df.loc[right_team]
    left_team_totals = left_team_data[[*comp_types]].agg('mean')
    right_team_totals = right_team_data[[*comp_types]].agg('mean')
    st.header('Left Team')
    st.write(left_team_data)

    st.header('Right Team')
    st.write(right_team_data)
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=left_team_totals.tolist(),
        theta=comp_types,
        fill='toself',
        name='Left Team'
    ))
    fig.add_trace(go.Scatterpolar(
        r=right_team_totals.tolist(),
        theta=comp_types,
        fill='toself',
        name='Right Team'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False
    )
    ct.write(fig)

st.header('All Hero Data')

st.write(heroes_df)
