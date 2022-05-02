from uuid import uuid4
from django.db import settings
from django.db import models
from django.db.models.aggregates import Sum


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(default=datetime.now())
    die = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

        def __str__(self):
            return "{}".format(self.name)


class MovieManager(models.Manager):
    def top_movies(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum("vote__value"))
        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by("-vote_sum")
        qs = qs[:limit]
        return qs

    def all_about_movie(self):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum("vote__value"))
        return qs

    def get_api(self, pk):
        from rest_framework.exceptions import ValidationError
        try:
            qs = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as ex:
            raise ValidationError(ex)
        return qs


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, "NR - Not Rated"),
        (RATED_G, "G - General Audiences"),
        (RATED_PG, "PG - Parental Guidance"),
        (RATED_R, "R - Restricted")
    )

    title = models.CharField(max_length=100)
    preview = models.TextField(max_length=5000)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    genre = models.CharField(null=True, max_length=100, db_index=True)
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    actors = models.ManyToManyField()

    objects = MovieManager()

    class Meta:
        ordering = ["-year", "title"]

    def __str__(self):
        return "{} ({})".format(self.title, self.year)


class VoteManager(models.Manager):
    def get_vote_or_blank_vote(self, movie):
        try:
            return Vote.objects.get(movie=movie)
        except Vote.DoesNotExist:
            return Vote(movie=movie)

    @staticmethod
    def api_get(pk=None):
        from rest_framework.exceptions import ValidationError
        try:
            queryset = Vote.objects.get(pk=pk)
        except Movie.DoesNotExist as e:
            raise ValidationError
        return queryset


class Vote(models.Model):
    like = 1
    dislike = -1
    value_choice = ((like, '+'), (dislike, '-'))
    value = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_vote',on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    objects = VoteManager()

    def __str__(self):
        return str(self.value
