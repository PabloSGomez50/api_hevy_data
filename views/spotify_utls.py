import requests
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.getenv('CLIENT_ID')
redirect_uri = 'http://localhost:8888/callback'