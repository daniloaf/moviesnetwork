# scripts/read_data.py
import os.path
import re

from django.db import transaction
from moviesdata.models import Actor, Cast, Movie

ACTORS_FILE_NAME = "actors.list"
ACTRESSES_FILE_NAME = "actresses.list"


class DataReader(object):
    '''
    '''
    current_objects = []

    def __init__(self, file_name):
        '''
        '''
        self.file_name = file_name

    def read_data(self):
        '''
        '''
        file_index = 1
        current_file_name = self.file_name + str(file_index)
        while os.path.isfile(current_file_name):
            self._process_file(current_file_name)
            file_index += 1
            current_file_name = self.file_name + str(file_index)

    @transaction.atomic
    def _process_file(self, current_file_name):
        print "============= Reading " + current_file_name + "============="
        with open(current_file_name, "r") as f:
            current_line_number = 1
            for line in f:
                if current_line_number % 1000 == 0:
                    print "Current line: %d (%s)" %\
                        (current_line_number, current_file_name)
                self._process_line(line)
                current_line_number += 1

    def _process_line(self, line):
        '''
        '''
        raise NotImplementedError("Abstract method")

    def _save_objects(self):
        for obj in self.current_objects:
            obj.save()
        self.current_objects = []


class ActorReader(DataReader):
    '''
    '''

    _GROUP_ACTOR = "actor"
    _GROUP_MOVIE = "movie"
    _GROUP_CAST = "cast"
    _current_actor = None

    actor_regex = re.compile(
        r"(?P<actor>[\w\W]+)\t(?P<movie>[\w\W]+)\s{2}\[(?P<cast>[\w\W]+)\]")

    def __init__(self, file_name):
        '''
        '''
        super(ActorReader, self).__init__(file_name)

    def _process_line(self, line):
        '''
        '''
        match = self.actor_regex.match(line)
        if match is not None:
            actor_name = match.group(self._GROUP_ACTOR).strip()
            movie_name = match.group(self._GROUP_MOVIE).strip()
            cast_name = match.group(self._GROUP_CAST).strip()

            try:
                if actor_name:
                    self._current_actor, created = Actor.objects.get_or_create(
                        name=actor_name.decode("latin-1").encode("utf-8"))
                    self._current_actor.save()

                movie, created = Movie.objects.get_or_create(
                    name=movie_name.decode("latin-1").encode("utf-8"))

                cast, created = Cast.objects.get_or_create(
                    character=cast_name.decode("latin-1").encode("utf-8"),
                    movie=movie,
                    actor=self._current_actor)
            except Exception, message:
                # print "Error on line"
                print message

        # else:
        #     print "Invalid line"


def run():
    actor_reader = ActorReader(ACTRESSES_FILE_NAME)
    actor_reader.read_data()
