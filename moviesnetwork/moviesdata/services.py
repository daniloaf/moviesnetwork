import imdb

from data import Actor


def search_actor(name):
    imdb_access = imdb.IMDb()
    result = imdb_access.search_person(name)
    actors = []
    if result:
        actors = [Actor.create(r, False) for r in result]
    return actors
