from django.db import models


class Team(models.Model):
    """
    Represents a cricket team
    """
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=50)
