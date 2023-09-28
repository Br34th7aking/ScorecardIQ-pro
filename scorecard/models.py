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


class MatchCategory(models.Model):
    """
    Represents a match type like ODI, T20, Test etc
    """

    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class Event(models.Model):
    """
    Represents a tour / series
    """

    name = models.CharField(max_length=100)
    season = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.season}"


class Person(models.Model):
    name = models.CharField(max_length=150)
    cricsheet_id = models.CharField(max_length=50)


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
class Match(models.Model):
    cricsheet_id = models.CharField(max_length=100, unique=True)
    event_id  = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_match_number = models.IntegerField()
    match_category_id = models.ForeignKey(MatchCategory, on_delete=models.CASCADE)
    venue_id  = models.ForeignKey(Venue, on_delete=models.CASCADE)
    gender  = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    overs = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    player_of_the_match = models.ManyToManyField(Person)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Toss(models.Model):
    """
    Represents the toss & result before the game.
    """
    winner = models.OneToOneField(Team, on_delete=models.CASCADE)
    decision = models.CharField(max_length=25)
    match_id = models.OneToOneField(Match, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Outcome(models.Model):
    """
    Represents the result of a game
    """
    match_id = models.OneToOneField(Match, on_delete=models.CASCADE)
    winner = models.OneToOneField(Team, on_delete=models.CASCADE)
    by = models.CharField(max_length=50)
    margin = models.CharField(max_length=25)
