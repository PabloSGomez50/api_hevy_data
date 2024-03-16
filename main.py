import os
import discord
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from views.hevy_utils import get_df
import routers
from labfra_bot import LabBot
import auth
from views import meli
from db import mysql
import logging

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX_BOT = os.getenv("PREFIX_BOT")
DISCORD_ACTIVE = int(os.getenv("DISCORD_ACTIVE", 0))


@asynccontextmanager
async def lifespan(app: FastAPI):
    df = get_df(data_dir)
    df.to_csv(os.path.join(data_dir, 'data.csv'))
    if DISCORD_ACTIVE:
        asyncio.create_task(bot.start(DISCORD_TOKEN))
    mysql.Base.metadata.create_all(bind=mysql.engine)

    yield
    print("Finished app")

app = FastAPI(lifespan=lifespan)
app.include_router(routers.hevy_router)
app.include_router(routers.meli_router)
# Bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = LabBot(intents=intents)

ALLOWED_HOSTS_DEFAULT = ','.join([
    "http://localhost:5173",
    "https://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
])

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ALLOWED_HOSTS_DEFAULT).replace(' ', '').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'data')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/meli/test/{search_text}")
def find_meli_posts(search_text: str):
    output = meli.search_ml_posts(search_text)
    return output

if __name__ == '__main__':
    # main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # pass