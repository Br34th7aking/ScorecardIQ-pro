from django.db import models


class Team(models.Model):
    """
    Represents a cricket team
    """
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Venue(models.Model):
    """
    Represents a cricket venue
    """
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.city}"