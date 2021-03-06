# from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication

from core.models import Movie, MovieManager, Actor, Vote, VoteManager
from .serializers import MovieSerializer, ActorSerializer, VoteSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# class MovieList(APIView):
#     """
#     View to list all movies in the system.
#
#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAdminUser]
# class MovieList(APIView):
#     def get(self, request, format=None):
#         """
#         Return a list of all movies
#         """
#         movies = [movie.title for movie in Movie.objects.all()]
#         return Response(movies)

class ReadOnly(BasePermission):
    def has_permission(self,request, view):
        return request.method in SAFE_METHODS

class MovieViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def paginate_movies_api(self, request, queryset):
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = MovieSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = MovieSerializer(queryset, many=True)
            return Response(serializer.data)


    @method_decorator(cache_page(60))
    def list(self, request):
        queryset = Movie.objects.all()
        return self.paginate_movies_api(request, queryset)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @method_decorator(cache_page(60))
    def retrieve(self, request, pk=None):
        queryset = Movie.objects.api_get(pk)

        serializer = MovieSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Movie.objects.api_get(pk)

        serializer = MovieSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    @method_decorator(cache_page(60))
    @action(methods=['get'], detail=False, name='Top movies')
    def top(self, request, limit=10):
        queryset = Movie.objects.top_movies(limit=limit)
        return self.paginate_movies_api(request, queryset)


class VoteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def update(self, request, parent_lookup_movie_id, pk=None):
        pk = parent_lookup_movie_id
        queryset = Vote.objects.api_get(pk)

        serializer = VoteSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
