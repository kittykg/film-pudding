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

        if len(r) > 1:
            for f in r:
                title = f["title"]
                release_year = datetime.strptime(
                    f["release_date"], "%Y-%m-%d").year
                if title == film_name and release_year == int(film_year):
                    return f["id"]
            return None
        else:
            return r[0]["id"]

    def _get_film_genres(self, id):
        api_path = F"/movie/{id}"
        url = self.base_URL + api_path

        PARAMS = {"api_key": self.api_key}

        genres = requests.get(url, PARAMS).json()["genres"]

        g_ids = []
        for g in genres:
            g_ids.append(g["id"])

        return g_ids

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
        id = self._get_film_id(film_name, film_year)

        if id == None:
            return None

        genres = self._get_film_genres(id)
        cast = self._get_film_cast(id)

        return genres, cast
