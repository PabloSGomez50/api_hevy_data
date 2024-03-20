from fastapi import Depends, APIRouter
from fastapi.security.api_key import APIKey

import os
import pandas as pd
import json
import views.hevy_utils as plots
import auth

hevy_router = APIRouter()

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

@hevy_router.get("/plots/{theme}")
def get_plots(theme: str = "", api_key: APIKey = Depends(auth.get_api_key)):
    """
    theme: ['ggplot2', 'seaborn', 'simple_white', 'plotly',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none']
    """
    df = pd.read_csv(os.path.join(data_dir, 'data.csv'))
    plot = plots.get_count_time_series(df, theme=theme)
    plot2 = plots.get_count_by_month(df, theme=theme)
    plot3 = plots.get_data_each_ej(df, theme=theme)
    data = [json.loads(p.to_json()) for p in [plot, plot2, plot3]]
    # print(data.keys())
    return data
