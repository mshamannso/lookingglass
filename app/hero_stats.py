# %%
import os
import sqlalchemy as sa
import pandas as pd

from app.database import engine

BASE_DIR = os.path.abspath(os.path.dirname('./'))
hero_stats_path = f'{BASE_DIR}\\data/hero_stats.csv'

# %%

def load_data(path) -> pd.DataFrame:
    data_frame = pd.read_csv(path)
    data_frame.set_index('HeroName', inplace=True)
    return data_frame

# %%

hero_stats = load_data(hero_stats_path)
