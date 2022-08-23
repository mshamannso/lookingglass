import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#%%
st.set_page_config(
    page_title="Scouting",
    page_icon="👋",
)

st.title('Scout')
st.sidebar.success("Select a demo above.")

#%%
def load_data():
    path = './data/TeamMapTotal.csv'
    df = pd.read_csv(path)
    return df

#%%
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')

# Names of ‘variable’ and ‘value’ columns can be customized
melted = pd.melt(data, id_vars =['MapName', 'TeamName'], value_vars =['Games', 'WinRate'])

st.write(melted)
# games_to_filter = 5
# filtered_data = data[data['Games'] >= games_to_filter]
# st.write(filtered_data)

# st.subheader('Raw Map data')
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
