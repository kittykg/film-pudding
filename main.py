import os
from tmdb_api import TmdbApiWrapper

API_KEY = os.environ['TMDB_API_KEY']

taw = TmdbApiWrapper(API_KEY)

g, c = taw.get_film_details("RoboCop", "2014")

print(g)
print(c)
