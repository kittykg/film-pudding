import numpy as np

from pudding_model.encoding_utils import genre_encode_one, cast_encode_one
from pudding_model.tmdb_api import TmdbApiWrapper


# Data format
# [year,  genres,   runtime, popularity, vote_avg, cast,  myrating]
#  float, special,  float,   float,      float,    float, float
class SingleDataProcessor:
    def __init__(self, api_key):
        self.taw = TmdbApiWrapper(api_key)

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
