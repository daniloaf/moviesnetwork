import imdb

from data import Actor


def search_actor(name):
    imdb_access = imdb.IMDb()
    result = imdb_access.search_person(name)
    actors = []
    if result is not None:
        for r in result:
            actors.append(Actor.create(r, False))
    return actors