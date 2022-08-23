import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Map Data", page_icon="📊")

st.markdown("# Map Totals")
st.sidebar.header("Map Totals")

@st.cache
def load_data() -> pd.DataFrame:
    path = './data/TeamMapTotal.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame


df = load_data()
teams = st.multiselect(
    "Choose teams", list(df.index.unique())
)

if not teams:
    st.error("Please select at least one team.")
else:
    data = df.loc[teams]

    data.reset_index(inplace=True)
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.7)
        .encode(
            x="MapName:N",
            y=alt.Y("Games:Q", stack=None),
            color="TeamName:N",
            tooltip=['TeamName', 'MapName', 'WinRate', 'Wins']
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.write("### Raw Data", data.sort_index())
