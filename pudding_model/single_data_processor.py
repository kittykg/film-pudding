import numpy as np

from .encoding_utils import genre_encode_one, cast_encode_one
from .tmdb_api import TmdbApiWrapper


# Data format
# [year,  genres,   runtime, popularity, vote_avg, cast,  myrating]
#  float, special,  float,   float,      float,    float, float
class SingleDataProcessor:
    def __init__(self):
        with open("pudding_model/secret_key", "r") as sk:
            API_KEY = sk.readline().splitlines().pop()
        sk.close()
        self.taw = TmdbApiWrapper(API_KEY)

    def film_to_input(self, film_name, film_year):
        assert len(film_name) > 0
        details = self.taw.get_film_details(film_name, film_year)
        if details is None:
            print("Can't find this film on TMDB")
            return None
        data = [film_year] + details

        genre_encoding = genre_encode_one(data[1])
        cast_encoding = cast_encode_one(data[5])

        x = [data[0]] + genre_encoding.tolist() + data[2:5] + [cast_encoding]

        return np.array(x).astype('float')
