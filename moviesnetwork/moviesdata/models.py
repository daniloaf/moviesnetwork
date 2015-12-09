from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField


class Actor(models.Model):

    name = models.CharField(blank=False, max_length=50, unique=True)
    casting = ListField(EmbeddedModelField('Cast'))

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"

    # def __str__(self):
        # return self.name.encode("utf-8")


class Movie(models.Model):

    name = models.CharField(blank=False, max_length=50, unique=True)
    cast = ListField(EmbeddedModelField('Cast'))

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    # def __str__(self):
        # return self.name.encode("utf-8")


class Cast(models.Model):

    character = models.CharField(blank=False, max_length=50)

    class Meta:
        verbose_name = "Cast"
        verbose_name_plural = "Casts"
        # unique_together = ("character", "movie", "actor")

    # def __str__(self):
        # return self.character.encode("utf-8") + " - " + self.movie.name.encode("utf-8") + "[" + self.actor.name.encode("utf-8") + "]"
