import csv
import numpy as np
from sklearn.preprocessing import LabelBinarizer

from tmdb_api import TmdbApiWrapper


# Data format
# [year,  genres,   runtime, popularity, vote_avg, cast,  myrating]
#  float, special,  float,   float,      float,    float, float
class DataProcessor:
    def __init__(self, api_key, file_name):
        self.taw = TmdbApiWrapper(api_key)
        self.film_data = None
        with open(file_name, newline="") as csvfile:
            rdr = csv.reader(csvfile, delimiter=",")
            self.n_y_r_list = [[row[1], row[2], row[4]] for row in rdr]

    def _gather_data(self):
        film_data = []
        for n_y_r in self.n_y_r_list:
            n, y, r = n_y_r
            details = self.taw.get_film_details(n, y)
            if details == None:
                continue
            new_data = [y] + details + [r]
            film_data.append(new_data)
        
        self.film_data = np.array(film_data)

    def _genre_encode(self, data):
        all_genres = self.taw.get_all_genres()
        lb = LabelBinarizer()
        lb.fit(all_genres)
        return [np.sum(lb.transform(d), axis=0) for d in data]

    def _cast_encode(self, data):
        favs = open('fav_cast.txt', 'r').read().splitlines()
        return [float(d in favs) for d in data]

    def _encode_data(self):
        columns = self.film_data.T
        encoded_columns = []
        for i in range(len(columns)):
            c = columns[i]
            # Genres
            if i == 1:
                encoded_columns.append(self._genre_encode(c))
            # Cast
            elif i == 5:
                encoded_columns.append(self._cast_encode(c))
            else:
                encoded_columns.append(c)
        encoded_data = np.array(encoded_columns).T
        
        result = []
        for d in encoded_data:
            list_d = list(d)
            print(list_d[0])
            new_d = [int(list_d[0])] + list(list_d[1]) + list_d[2:]
            print(new_d)
            result.append(new_d)

        return np.array(result)


    def processe_data(self):
        self._gather_data()
        return self._encode_data()
        
    def write_to_file(self, data):
        np.savetxt("processed_data.csv", data, delimiter=",", newline="\n")
