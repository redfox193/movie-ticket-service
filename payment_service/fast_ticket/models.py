from django.db import models


class History(models.Model):
    film = models.CharField(max_length=100)
    email = models.EmailField()
    code = models.CharField(max_length=10)
    date = models.DateField(max_length=100)

