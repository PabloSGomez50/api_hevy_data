import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_dark"
peso_corporal = 68.7

def get_count_time_series(df):
    data = df.groupby('start_time').agg({'exercise_title': 'count', 'weight_kg': 'mean'})\
            .rename({'exercise_title': 'exercise_count'}, axis=1)
    data['weight_kg'] = data['weight_kg'].round(2)
    fig = px.scatter(data, x=data.index, y='exercise_count', 
                color='weight_kg', 
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

def get_count_by_month(df):
    data = df.groupby(['m-y', 'title']).agg({'exercise_title': 'count', 'weight_kg': 'mean'})\
        .rename({'exercise_title': 'exercise_count'}, axis=1)
    data['weight_kg'] = data['weight_kg'].round(2)
    data = data.reset_index(level='title')

    fig = px.bar(data, x=data.index, y='exercise_count', 
            color='weight_kg', 
            facet_col='title',
            # marginal_x="histogram"
            barmode='group',
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

def get_data_each_ej(df):
    operations = ['max', 'min', 'mean']
    data = df.groupby(['title', 'exercise_title']).agg({
        'weight_kg': operations
    }).fillna(peso_corporal)
    data = data.droplevel(1, axis=1)
    data.columns = [f'peso_{op}'for op in operations]
    data = data.reset_index(level='title')
    fig = px.bar(data, x=data.index, y='peso_mean')
    return fig