import numpy as np
from sklearn.preprocessing import LabelBinarizer

from tmdb_api import TmdbApiWrapper

with open("secert_key", "r") as sk:
    API_KEY = sk.readline().splitlines().pop()
sk.close()

taw = TmdbApiWrapper(API_KEY)
all_genres = taw.get_all_genres()
lb = LabelBinarizer()
lb.fit(all_genres)


def genre_encode(data):
    for i, d in enumerate(data):
        if len(d) == 0:
            print(F"rip {i}")
    return [np.sum(lb.transform(d), axis=0) for d in data]


def genre_encode_one(data):
    return np.sum(lb.transform(data), axis=0)


def cast_encode(data):
    with open('fav_cast.txt', 'r') as fav_cast:
        favs = fav_cast.read().splitlines()
        encoding = [float(len(list(filter(lambda a: a in favs, d))))
                    for d in data]
    fav_cast.close()
    return encoding


def cast_encode_one(data):
    with open('fav_cast.txt', 'r') as fav_cast:
        favs = fav_cast.read().splitlines()
        encoding = float(len(list(filter(lambda a: a in favs, data))))
    fav_cast.close()
    return encoding
