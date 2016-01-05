from django.test import TestCase
from imdb.Person import Person
from imdb.Movie import Movie as IMDbMovie

from moviesdata.serializers import\
    SearchActorSerializer, ActorSerializer, MovieSerializer
from moviesdata.data import Actor, Movie


class SearchActorSerializerTests(TestCase):

    def test__serialize__actor_search_result__serialized_data(self):
        # Arrange
        actors = [Actor(1, 'Actor1'), Actor(2, 'Actor2')]
        expected_actors = [
            {'actor_id': 1, 'name': 'Actor1'}, {'actor_id': 2, 'name': 'Actor2'}
        ]
        # Act
        serializer = SearchActorSerializer(actors, many=True)
        # Assert
        self.assertEqual(serializer.data, expected_actors)


class MovieSerializerTests(TestCase):

    def test__serializer__full_movie__serialized_data(self):
        # Arrange
        movie = Movie.create(IMDbMovie(
            movieID=1,
            data={
                'title': 'mymovie',
                'year': 2015,
                'kind': 'movie',
                'rating': 10,
                'cover url': 'cover'
            }),
            True)
        expected_movie = {
            'movie_id': 1,
            'title': 'mymovie',
            'year': 2015,
            'rating': 10,
            'cover': 'cover'
        }
        # Act
        serializer = MovieSerializer(movie)
        # Assert
        self.assertEqual(serializer.data, expected_movie)


class ActorSerializerTests(TestCase):

    def test__serialize__full_actor__serialized_data(self):
        # Arrange
        actor = Actor.create(
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
                                'year': 2015, 'kind': 'movie'
                            })
                    ]
                }
            ),
            True
        )
        expected_actor = {
            'actor_id': 1,
            'name': 'Actor1',
            'headshot': 'hs',
            'movies': [
                {
                    'movie_id': 1,
                    'title': 'mymovie',
                    'year': 2015,
                    'rating': None,
                    'cover': None}
            ]
        }
        # Act
        serializer = ActorSerializer(actor)
        # Assert
        self.assertEqual(serializer.data, expected_actor)
