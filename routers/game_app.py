from fastapi import Depends, APIRouter
from fastapi.security.api_key import APIKey
import auth

game_router = APIRouter()

@game_router.get("/games")
def get_game_status(api_key: APIKey = Depends(auth.get_api_key)):
    games = {
        'mafia': 1,
        'pool': 5,
        'adivina_quien_es': 2,
        'truco': 5
    }
    return games

# @game_router.get("/games/rooms")
# def get_rooms(api_key: APIKey = Depends(auth.get_api_key)):
#     rooms = firebase.get_actives()

#     return rooms