from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone
from datetime import date
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Running', duration=30, date=date.today())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=date.today())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=date.today())
        Activity.objects.create(user=users[3], type='Yoga', duration=40, date=date.today())

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
        w2 = Workout.objects.create(name='Agility Training', description='Agility workout for heroes')
        w1.suggested_for.set(users)
        w2.suggested_for.set(users)

        self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on email field...'))
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.user.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
