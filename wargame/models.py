from django.db import models

class Player(models.model):
    name = models.CharField(max_length=25)
    wins = models.PositiveIntegerField()

