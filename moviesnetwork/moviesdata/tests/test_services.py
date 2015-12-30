import mock

from django.test import TestCase
from imdb.Person import Person
from imdb.Movie import Movie as IMDbMovie

from moviesdata.data import Actor
from moviesdata.services import search_actor, get_actor_info


class ServicesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ServicesTests, cls).setUpClass()
        cls.imdb_search_person_patcher = mock.patch('imdb.parser.http.IMDbHTTPAccessSystem.search_person')
        cls.imdb_get_person_patcher = mock.patch('imdb.parser.http.IMDbHTTPAccessSystem.get_person')
        cls.imdb_search_person_mock = cls.imdb_search_person_patcher.start()
        cls.imdb_get_person_mock = cls.imdb_get_person_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.imdb_search_person_patcher.stop()
        cls.imdb_get_person_patcher.stop()
        super(ServicesTests, cls).tearDownClass()

    def test__search_actors__actors_found__actors_list(self):
        # Arrange
        self.imdb_search_person_mock.return_value = [
            Person(personID=1, name='Actor1'), Person(personID=2, name='Name2')
        ]
        # Act
        actors = search_actor('myname')
        # Assert
        self.assertEquals(actors, [Actor(1, 'Actor1'), Actor(2, 'Name2')])

    def test__search_actors__None_returned__empty_list(self):
        # Arrange
        self.imdb_search_person_mock.return_value = None
        # Act
        actors = search_actor('myname')
        # Assert
        self.assertEquals(actors, [])

    def test__get_actor_info__actor_found__actor(self):
        # Arrange
        person = Person(
            personID=1,
            data={
                'name': 'Actor1',
                'headshot': 'hs',
                'actor': [
                    IMDbMovie(movieID=1, data={'title': 'mymovie', 'year': 2015, 'kind': 'movie'})
                ]
            }
        )
        self.imdb_get_person_mock.return_value = person
        expected_actor = Actor.create(person, True)
        # Act
        actor = get_actor_info(1)
        # Assert
        self.assertEquals(actor, expected_actor)

    def test__get_actor_info__actor_not_found__None(self):
        # Arrange
        personID = 1
        self.imdb_get_person_mock.return_value = Person(personID=personID, data={})
        # Act
        actor = get_actor_info(personID)
        # Assert
        self.assertIsNone(actor)
