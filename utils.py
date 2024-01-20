import pandas as pd
import numpy as np
import os

def get_df(data_dir):
    # df = pd.concat([pd.read_csv(os.path.join(data_dir, fn), sep=';') 
    #         for fn in os.listdir(data_dir)])
    df = pd.read_csv(os.path.join(data_dir, 'workouts.csv'), sep=';')

    return clean_data(df)

def fix_alingment(df):
    error_index = df[(df['end_time'] == 'normal') | df['end_time'].isna()].index
    for idx in error_index:
        i = 0
        while df.loc[idx - i, 'end_time'] == 'normal' or df.loc[idx - i, 'end_time'] is np.NaN:
            i += 1
        df.loc[idx - i, 'exercise_notes'] = df.loc[idx - i, 'exercise_notes'].replace('"', '') + df.loc[idx, 'title'].replace('"', '')
        df['weight_kg'] = df['weight_kg'].astype(float)
        df.loc[idx - i, 'set_index':'reps'] = df.loc[idx, 'start_time':'exercise_title'].values

    return df.drop(error_index).reset_index(drop=True)

def clean_data(df):
    """Limpiar los datos obtenidos desde hevy"""

    df = fix_alingment(df).copy()
    df.start_time = pd.to_datetime(df['start_time'], format='%d %b %Y, %H:%M')
    df.end_time = pd.to_datetime(df['end_time'], format='%d %b %Y, %H:%M')
    df['day'] = df.start_time.dt.day
    df['month'] = df.start_time.dt.month
    df['year'] = df.start_time.dt.year
    df['m-y'] = df.start_time.dt.strftime('%m-%Y')
    df['set_index'] = df['set_index'].astype(int) + 1
    df['reps'] = df['reps'].fillna(1).astype(int)
    df['weight_kg'] = df['weight_kg'].astype(float)
    df = df.dropna(how='all', axis=1)
    return df