import imdb

from data import Actor


def search_actor(name):
    """
    Searches for actors in IMDb and return a list of Actor.
    """
    imdb_access = imdb.IMDb()
    result = imdb_access.search_person(name)
    actors = [Actor.create(r, False) for r in result] if result else []
    return actors


def get_actor_info(actor_id):
    """
    Returns Actor with full info from IMDb.
    """
    imdb_access = imdb.IMDb()
    result = imdb_access.get_person(actor_id)
    actor = Actor.create(result, True) if result.data else None
    return actor
