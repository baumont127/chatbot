import resource
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Ressource(models.Model):
    date = models.DateField(default= now())
    titre = models.CharField(max_length=100)
    lien = models.URLField(max_length=300)
    key_word = models.CharField(max_length=100, blank=True)
    ressource = models.ForeignKey('Type_ressource', on_delete=models.SET_NULL, null=True)
    corpus = models.TextField(max_length=5000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.ressource} {self.titre}")   
    

class Type_ressource(models.Model):
    RESSOURCE = [
        ('Video', 'Video'),
        ('Article', 'Article'),
    ]

    name = models.CharField(max_length=100, choices=RESSOURCE)

    def __str__(self):
        return (f"{self.name}")
