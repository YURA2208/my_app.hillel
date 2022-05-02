from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import Movie, Actor, Vote
from movie_api.serializers import MovieSerializer
from rest_framework import status


class MovieApiTestCase(APITestCase):

    def test_get_movie(self):
        url = reverse("movie_api:movies-list")
        movie1 = Movie.objects.create(title="Avengers",
                                      year=2012, rating=1, runtime=120, preview="Action movie")
        movie2 = Movie.objects.create(title="Avengers:Age of Ultron",
                                      year=2015, rating=1, runtime=140, preview="Action movie")
        response = self.client.get(url)
        data = MovieSerializer([movie1, movie2], many=True).data
        self.assertEqual(data, response.data["results"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post_movie(self):
        url = reverse("movie_api:movies-list")
        data = {
            "title": "Avengers",
            "year": 2012,
            "rating": 1,
            "runtime": 120,
            "preview": "Action movie",
            "actors": [],
            "vote": []
        }
        response = self.factory.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201)
        self.assertEqual(data, response.data)