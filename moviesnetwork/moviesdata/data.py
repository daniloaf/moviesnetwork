class Actor(object):

    def __init__(self, actor_id, name):
        self.actor_id = actor_id
        self.name = name
        self.movies = []

    @staticmethod
    def create(imdb_person, full_info):
        actor = Actor(imdb_person.getID(), imdb_person.data['name'])
        if full_info:
            actor.movies = imdb_person.data['actor']

        return actor

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.actor_id == other.actor_id and self.name == other.name
