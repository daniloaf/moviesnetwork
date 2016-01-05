import imdb
from django.core.cache import cache

from data import Actor


CACHE_EXPIRATION_TIME = 60 * 60 * 24 * 7  # One week
ACTOR_CACHE_KEY_PREFIX = 'actor_'
MOVIE_CACHE_KEY_PREFIX = 'movie_'


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
    cache_key = ACTOR_CACHE_KEY_PREFIX + str(actor_id)
    actor = cache.get(cache_key)
    if not actor:
        imdb_access = imdb.IMDb()
        result = imdb_access.get_person(actor_id)
        actor = Actor.create(result, True) if result.data else None
        cache.set(cache_key, actor, CACHE_EXPIRATION_TIME)
    return actor
