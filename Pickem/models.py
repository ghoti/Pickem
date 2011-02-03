from django.db import models
from django.contrib.auth.views import User

# Create your models here.
TEAMS = (
    ('BAL', 'Baltimore Ravens'),
    ('CIN', 'Cincinnati Bengals'),
    ('CLE', 'Cleveland Browns'),
    ('PIT', 'Pittsburgh Steelers'),
    ('CHI', 'Chicago Bears'),
    ('DET', 'Detroit Lions'),
    ('GB', 'Green Bay Packers'),
    ('MIN', 'Minnesota Vikings'),
    ('HOU', 'Houston Texans'),
    ('IND', 'Indianapolis Colts'),
    ('JAX', 'Jacksonville Jaguars'),
    ('TEN', 'Tennessee Titans'),
    ('ATL', 'Atlanta Falcons'),
    ('CAR', 'Carolina Panthers'),
    ('NO', 'New Orleans Saints'),
    ('TB', 'Tampa Bay Buccaneers'),
    ('BUF', 'Buffalo Bills'),
    ('MIA', 'Miami Dolphins'),
    ('NE', 'New England Patriots'),
    ('NYJ', 'New York Jets'),
    ('DAL', 'Dallas Cowboys'),
    ('NYG', 'New York Giants'),
    ('PHI', 'Philadelphia Eagles'),
    ('WAS', 'Washington Redskins'),
    ('DEN', 'Denver Broncos'),
    ('KC', 'Kansas City Chiefs'),
    ('OAK', 'Oakland Raiders'),
    ('SD', 'San Diego Chargers'),
    ('ARZ', 'Arizona Cardinals'),
    ('SF', 'San Francisco 49ers'),
    ('SEA', 'Seattle Seahawks'),
    ('STL', 'St. Louis Rams')
    )

class Profile(models.Model):
    user =models.IntegerField()
    w = models.IntegerField()
    l = models.IntegerField()

class Team(models.Model):
    call = models.CharField(max_length=3)
    city = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    w = models.IntegerField()
    l = models.IntegerField()

    def __unicode__(self):
        return self.name

class Game(models.Model):
    week = models.IntegerField()
    away = models.CharField(max_length=3)
    home = models.CharField(max_length=3)
    homescore = models.IntegerField(blank=True, null=True)
    awayscore = models.IntegerField(blank=True, null=True)

class Pick(models.Model):
    user = models.IntegerField()
    week = models.IntegerField()
    game = models.IntegerField()
    pick = models.IntegerField()
