from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from core.models import Movie, Actor


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--len', type=int, default=10)
        parser.add_argument('--year', type=int, default=2000)


    def handle(self, *args, **options):
        self.stdout.write('Start adding films')
        faker = Faker()


        for _ in range(options['len']):
            self.stdout.write('Start adding films')
            movie = Movie()
            movie.title = ' '.join(faker.text().split()[:4])
            movie.plot = faker.text()
            movie.runtime = 180
            movie.rating = randint(-100, 100)
            movie.year = options['year']
            movie.save()

            for _ in range(randint(1, 10)):
                actor = Actor()
                actor.first_name = ' '.join(faker.name().split()[:1])
                actor.last_name = ' '.join(faker.name().split()[1:])
                # actor.name = faker.name_actor
                actor.save()
                movie.actors.add(actor)

            self.stdout.write(f'New movie: {movie.title}')
        self.stdout.write('END')




