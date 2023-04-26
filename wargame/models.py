from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=25)
    wins = models.PositiveIntegerField(default=0)

