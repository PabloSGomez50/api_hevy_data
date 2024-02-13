import pytest
import sys
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

# class TestPerson(unittest.TestCase):
#     pass

def test_index():
    r = requests.get('http://localhost:8000')
    assert r.status_code == 200
    assert r.text == '{"Hello":"World"}'

def test_plots():
    r = requests.get('http://localhost:8000/plots/plotly_dark')
    assert r.status_code == 403
    
    r2 = requests.get('http://localhost:8000/plots/plotly_dark', headers={
        "accept": "application/json",
        "access_token": API_KEY,
    })

    assert r2.status_code == 200