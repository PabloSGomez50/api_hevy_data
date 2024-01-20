import pandas as pd
import os
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from utils import get_df 
import plots

app = FastAPI()

ALLOWED_HOSTS = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "https://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'data')

@app.on_event("startup")
def startup():
    df = get_df(data_dir)
    df.to_csv(os.path.join(data_dir, 'data.csv'))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/plots/{username}")
def get_plots(username: str):
    df = pd.read_csv(os.path.join(data_dir, 'data.csv'))
    plot = plots.get_count_time_series(df)
    plot2 = plots.get_count_by_month(df)
    plot3 = plots.get_data_each_ej(df)
    data = [json.loads(p.to_json()) for p in [plot, plot2, plot3]]
    # print(data.keys())
    return data

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    # main()
    pass