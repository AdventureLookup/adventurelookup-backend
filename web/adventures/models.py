from django.db import models
from adventures.fields import *

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Adventure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    authors = models.ManyToManyField(Author)
    links = URLListField(default=[])

    def __str__(self):
        return self.name
