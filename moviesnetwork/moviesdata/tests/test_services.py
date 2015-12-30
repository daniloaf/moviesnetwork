import mock

from django.test import TestCase
from imdb.Person import Person

from moviesdata.data import Actor
from moviesdata.services import search_actor


class ServicesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ServicesTests, cls).setUpClass()
        cls.imdb_search_person_patcher = mock.patch('imdb.parser.http.IMDbHTTPAccessSystem.search_person')
        cls.imdb_search_person_mock = cls.imdb_search_person_patcher.start()

    def test__search_actors__actors_found__actors_list(self):
        # Arrange
        self.imdb_search_person_mock.return_value = [
            Person(personID=1, name='Actor1'), Person(personID=2, name='Name2')]
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
