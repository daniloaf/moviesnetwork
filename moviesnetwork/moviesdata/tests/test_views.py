import mock

from imdb.Person import Person
from imdb.Movie import Movie as IMDbMovie
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from moviesdata.urls import SEARCH_ACTOR, ACTOR
from moviesdata.data import Actor


class SearchActorViewTests(APITestCase):

    url = reverse(SEARCH_ACTOR)
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        super(SearchActorViewTests, cls).setUpClass()
        cls.services_patcher = mock.patch('moviesdata.views.search_actor')
        cls.service_mock = cls.services_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.services_patcher.stop()
        super(SearchActorViewTests, cls).tearDownClass()

    def test__get__actors_found__status_200(self):
        # Arrange
        self.service_mock.return_value = [
            Actor(1, 'Actor1'), Actor(2, 'Actor2')]
        request_params = {'name': 'my_name'}
        # Act
        response = self.client.get(self.url, request_params)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__get__actors_not_found__status_200(self):
        # Arrange
        self.service_mock.return_value = []
        request_params = {'name': 'my_name'}
        # Act
        response = self.client.get(self.url, request_params)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__get__name_not_passed__status_400(self):
        # Arrange
        request_params = {}
        # Act
        response = self.client.get(self.url, request_params)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test__get__actors_found__actors_in_response(self):
        # Arrange
        self.service_mock.return_value = [
            Actor(1, 'Actor1'), Actor(2, 'Actor2')]
        request_params = {'name': 'my_name'}
        # Act
        response = self.client.get(self.url, request_params)
        # Assert
        self.assertEqual(len(response.data), 2)


class ActorViewTests(APITestCase):

    url = reverse(ACTOR, kwargs={'actor_id': 1})
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        super(ActorViewTests, cls).setUpClass()
        cls.services_patcher = mock.patch('moviesdata.views.get_actor_info')
        cls.service_mock = cls.services_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.services_patcher.stop()
        super(ActorViewTests, cls).tearDownClass()

    def test__get__actor_found__status_200(self):
        # Arrange
        self.service_mock.return_value = Actor.create(
            Person(
                personID=1,
                data={
                    'name': 'Actor1',
                    'headshot': 'hs',
                    'actor': [
                        IMDbMovie(
                            movieID=1,
                            data={
                                'title': 'mymovie',
                                'year': 2015,
                                'kind': 'movie'
                            })
                    ]
                }
            ),
            True
        )
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__get__actor_not_found__status_404(self):
        # Arrange
        self.service_mock.return_value = None
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
