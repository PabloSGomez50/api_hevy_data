import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

MEAN_WEIGHT = float(os.getenv("MEAN_WEIGHT", 68.7))

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
        df.loc[idx - i, 'exercise_notes'] = df.loc[idx - i, 'exercise_notes'].replace('"', '') + '\n' + df.loc[idx, 'title'].replace('"', '')

        df.loc[idx - i, 'set_index':'reps'] = df.loc[idx, 'start_time':'exercise_title'].convert_dtypes().values

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
    df['set_index'] = df['set_index'].fillna(-1).astype(int) + 1
    df['reps'] = df['reps'].fillna(1).astype(int)
    df['weight_kg'] = df['weight_kg'].astype(float)
    df = df.dropna(how='all', axis=1)
    return df


def get_count_time_series(df, theme: str = "plotly_dark"):
    data = df.groupby('start_time').agg({'exercise_title': 'count', 'weight_kg': 'mean'})\
            .rename({'exercise_title': 'exercise_count'}, axis=1)
    data['weight_kg'] = data['weight_kg'].round(2)
    fig = px.scatter(data, x=data.index, y='exercise_count', 
                color='weight_kg',
                template=theme,
                # marginal_x="histogram"
                )

    fig.update_traces(
        marker=dict(
            size=14,
            opacity=0.75,
            line=dict(width=1, color='white')
        ),
        selector=dict(mode='markers')
    )

    # Layout customization
    fig.update_layout(
        title='Cantidad de ejercicios por día',
        xaxis_title='Fecha',
        yaxis_title='Total de ejercicios',
        legend_title='Pesos (kg)',
        coloraxis_colorbar=dict(title='Pesos (kg)'),
        # plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        # paper_bgcolor='rgb(255, 255, 255)',  # Set paper background color to white
        font=dict(size=12), # , color='black'
        # title_font_family='Open Sans'
    )
    return fig

def get_count_by_month(df, theme: str = "plotly_dark"):
    data = df.groupby(['m-y', 'title']).agg({'exercise_title': 'count', 'weight_kg': 'mean'})\
        .rename({'exercise_title': 'exercise_count'}, axis=1)
    data['weight_kg'] = data['weight_kg'].round(2)
    data = data.reset_index(level='title')

    fig = px.bar(data, x=data.index, y='exercise_count', 
            color='weight_kg', 
            facet_col='title',
            # marginal_x="histogram"
            barmode='group',
            template=theme,
            )

    for i in range(len(fig['data'])):
        fig.update_xaxes(title_text='Fecha', row=1, col=i+1)
    fig.update_layout(
        title='Cantidad de ejercicios por mes y por tipo',
        yaxis_title='Total de ejercicios',
        legend_title='Pesos (kg)',
        coloraxis_colorbar=dict(title='Pesos (kg)'),
        font=dict(size=12),
    )
    return fig

def get_data_each_ej(df, peso_corporal: float = MEAN_WEIGHT, theme: str = "plotly_dark"):
    operations = ['max', 'min', 'mean']
    data = df.groupby(['title', 'exercise_title']).agg({
        'weight_kg': operations
    }).fillna(peso_corporal)
    data = data.droplevel(1, axis=1)
    data.columns = [f'peso_{op}'for op in operations]
    data = data.reset_index(level='title')
    fig = px.bar(data, x=data.index, y='peso_mean', template=theme)
    return fig