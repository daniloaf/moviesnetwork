class Actor(object):
    """
    Represents an actor from IMDb.
    """

    def __init__(self, actor_id, name):
        self.actor_id = actor_id
        self.name = name
        self.movies = []
        self.headshot = None

    @staticmethod
    def create(imdb_person, full_info):
        """
        Creates a new actor using an imdb.Person.Person instance.

        full_info: False for id and name only. True for more info.
        """
        actor = Actor(imdb_person.getID(), imdb_person.data['name'])
        if full_info:
            for movie in imdb_person.data.get('actor', []):
                if movie.data['kind'] == 'movie':
                    actor.movies.append(Movie.create(movie, False))
            actor.headshot = imdb_person.get('headshot')

        return actor

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.actor_id == other.actor_id and self.name == other.name


class Movie(object):
    """
    Represents a movie from IMDb.
    """

    def __init__(self, movie_id, title, year):
        self.movie_id = movie_id
        self.title = title
        self.year = year
        self.rating = None
        self.cover = None

    @staticmethod
    def create(imdb_movie, full_info):
        """
        Creates a new actor using an imdb.Person.Person instance.

        full_info: False for id, title and year only. True for more info.
        """
        movie_data = imdb_movie.data
        movie = Movie(imdb_movie.getID(), movie_data['title'], movie_data['year'])
        if full_info:
            movie.rating = movie_data.get('rating')
            movie.cover = movie_data.get('cover url')
        return movie
