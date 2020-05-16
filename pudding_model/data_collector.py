import csv
import numpy as np

from pudding_model.tmdb_api import TmdbApiWrapper


# Data format
# [year,  genres,   runtime, popularity, vote_avg, cast,  myrating]
#  float, special,  float,   float,      float,    float, float
class DataCollector:
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
            if details is None:
                continue
            new_data = [y] + details + [r]
            film_data.append(new_data)

        self.film_data = np.array(film_data)

    def _write_to_file(self, output_file_name):
        np.save(output_file_name, self.film_data)

    def collect(self, output_file_name):
        self._gather_data()
        self._write_to_file(output_file_name)
