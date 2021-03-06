# Film Pudding

![kittykg](https://circleci.com/gh/kittykg/film-pudding.svg?style=svg
)

My taste of films is weird, so can ML predict if I'm going to like a flim or not?

## Data Source

All the ratings are from my Letterboxd. And the details are from TMDB.

Follow me on [Letterboxd](https://letterboxd.com/KittyG/) :P 

## Data Format

There are in total 24 input features and 1 output
1.  Year -- float
2.  Genres -- Label binary encoding
    1. Action
    2. Adventure
    3. Animation
    4. Comedy
    5. Crime
    6. Documentary
    7. Drama
    8. Family
    9. Fantasy
    10. History
    11. Horror
    12. Music
    13. Mystery
    14. Romance
    15. Science Fiction
    16. TV Movie
    17. Thriller
    18. War
    19. Western
3. Runtime -- float
4. Popularity -- float
5. Vote average -- float
6. Cast -- float (how many actors/actress are there in the film that are also my favourites)
*  My rating -- float

## Special files, exist only locally

*  fav_cast.txt
*  rating.csv
*  secret_key

## How to run the server

Run as DEV mode with hot-reloading:

`FLASK_ENV=dev FLASK_APP=pudding_server.py FLASK_DEBUG=True flask run`

Run with Gunicorn (change the IP if you want):

`gunicorn pudding_server:app --bind 0.0.0.0:5000`
