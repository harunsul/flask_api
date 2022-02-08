import requests
from flask_restful import reqparse
from werkzeug.wrappers import response

BASE = "http://127.0.0.1:5000/"

songs = {}

def show_songs():
    songs.clear()
    for i in range(10):
        song = requests.get(BASE + "song/" + str(i)).json()
        print(song)
        if i not in songs:
            songs[i] = song
        if "message" in song:
            del songs[i]
            break
    return songs

def increase_plays(i):
    response = requests.get(BASE + "song/" + str(i)).json()
    update = requests.patch(BASE + "song/" + str(i), {"plays": response["plays"]+1})
    return update.json()


def fill_database():
    data = [{"likes": 10, "name": "Song 1", "plays": 10000},
            {"likes": 78, "name": "Song 2", "plays": 900000},
            {"likes": 50, "name": "Song 3", "plays": 1500}]

    for i in range(len(data)):
        response = requests.put(BASE + "song/" + str(i), data[i])
        print(response.json())
