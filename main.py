import pandas as pd
import os
import json
import discord
import asyncio
from typing import Union

from fastapi import Depends, FastAPI
# from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils import get_df
from labfra_bot import LabBot
import auth
import plots

app = FastAPI()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX_BOT = os.getenv("PREFIX_BOT")
# Bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = LabBot(intents=intents)

ALLOWED_HOSTS = [
    "http://localhost:5173",
    "https://127.0.0.1",
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
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
    asyncio.create_task(bot.start(DISCORD_TOKEN))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/plots/{theme}")
def get_plots(theme: str = "", api_key: APIKey = Depends(auth.get_api_key)):
    df = pd.read_csv(os.path.join(data_dir, 'data.csv'))
    plot = plots.get_count_time_series(df, theme=theme)
    plot2 = plots.get_count_by_month(df, theme=theme)
    plot3 = plots.get_data_each_ej(df, theme=theme)
    data = [json.loads(p.to_json()) for p in [plot, plot2, plot3]]
    # print(data.keys())
    return data

if __name__ == '__main__':
    # main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # pass