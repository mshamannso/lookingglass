import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Hero Data", page_icon="📊")

st.markdown("# Hero Totals")
st.sidebar.header("Hero Totals")

@st.cache
def load_data() -> pd.DataFrame:
    path = './data/TeamMapTotal.csv'
    data_frame = pd.read_csv(path)
    data_frame.set_index('TeamName', inplace=True)
    return data_frame

st.write("### Raw Data", load_data())
