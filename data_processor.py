import numpy as np

from encoding_utils import genre_encode, cast_encode
from tmdb_api import TmdbApiWrapper


# Data format
# [year,  genres,   runtime, popularity, vote_avg, cast,  myrating]
#  float, special,  float,   float,      float,    float, float
class DataProcessor:
    def __init__(self, api_key, file_name):
        self.film_data = np.load(file_name, allow_pickle=True)
        self.taw = TmdbApiWrapper(api_key)

    def process_data(self):
        columns = self.film_data.T
        encoded_x = []
        normalised_y = columns[6].astype('float') / 5
        for i in range(len(columns)):
            c = columns[i]
            # Genres
            if i == 1:
                encoded_x.append(genre_encode(c))
            # Cast
            elif i == 5:
                encoded_x.append(cast_encode(c))
            elif i == 6:
                continue
            else:
                encoded_x.append(c)
        encoded_data = np.array(encoded_x).T

        final_x = []
        for d in encoded_data:
            list_d = list(d)
            new_d = [list_d[0]] + list(list_d[1]) + list_d[2:]
            new_d = [float(i) for i in new_d]
            final_x.append(new_d)

        return np.array(final_x), normalised_y
