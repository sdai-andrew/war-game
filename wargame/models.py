from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    wins = models.PositiveIntegerField(default=0)

