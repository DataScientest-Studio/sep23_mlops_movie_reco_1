from fastapi.testclient import TestClient
import pandas as pd
from main import app
import pytest
import warnings
warnings.filterwarnings('ignore')
import requests

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c

@pytest.fixture(scope="module")
def test_user():
    return {"username": 2, "password": "2"}

def test_login(client, test_user):
    response = client.post("/token", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"greetings": "welcome"}


def test_movie_recommendation_via_user(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/movie_recomendation_via_movie/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    from main import get_movie_from_user
    assert isinstance(response.json(), dict)

def test_movie_reco(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/movie_recomendation_via_movie/4162", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_check_user_exists(client, test_user):
    token = test_login(client, test_user)
    response =  client.get("/check_user_exist/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_check_movie_exists(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/check_movie_exist/128715", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_check_movie_doesnt_exists(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/check_movie_exist/128716", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_check_movie_rating(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/add_user/movieid/12/rating/5", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_show_db_data(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/add_user/movieid/12/rating/5", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_show_score(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/show_scores/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_delete_user(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/delete_user/10032", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_delete_movie(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/delete_movie/2478", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400


def test_user_exist(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/check_user_exist/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200