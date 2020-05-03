import requests
from datetime import datetime


class TmdbApiWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_URL = "https://api.themoviedb.org/3"

    def _get_film_id(self, film_name, film_year):
        api_path = "/search/movie"
        url = self.base_URL + api_path

        PARAMS = {
            "api_key": self.api_key,
            "query": film_name,
            "year": film_year
        }

        r = requests.get(url, PARAMS).json()["results"]

        if len(r) == 0:
            return None

        return r[0]["id"]

    def _get_film_detail(self, id):
        api_path = F"/movie/{id}"
        url = self.base_URL + api_path

        PARAMS = {"api_key": self.api_key}

        r = requests.get(url, PARAMS).json()

        genres = [g["name"] for g in r["genres"]]
        runtime = r["runtime"]
        popularity = r["popularity"]
        vote_avg = r["vote_average"]

        return [genres, runtime, popularity, vote_avg]

    def _get_film_cast(self, id):
        api_path = F"/movie/{id}/credits"
        url = self.base_URL + api_path

        PARAMS = {"api_key": self.api_key}

        cast = requests.get(url, PARAMS).json()["cast"]

        cast_names = []

        for c in cast:
            cast_names.append(c["name"])

        return cast_names

    def get_film_details(self, film_name, film_year):
        print(film_name)
        id = self._get_film_id(film_name, film_year)

        if id == None:
            print(film_name)
            return None

        d = self._get_film_detail(id)
        cast = self._get_film_cast(id)

        if len(d[0]) == 0:
            print(F"{film_name} has no genres")
            return None

        details = d.copy()
        details.append(cast)

        return details

    def get_all_genres(self):
        api_path = "/genre/movie/list"
        url = self.base_URL + api_path

        PARAMS = {"api_key": self.api_key}

        genres = requests.get(url, PARAMS).json()["genres"]
        return [g["name"] for g in genres]
