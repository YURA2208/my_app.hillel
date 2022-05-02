from django.urls import path, include
from . import views

app_name = "movie_auth"

urlpatterns = [
    path("", views.sign_in, name="sign_in"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("logout/", views.logout, name="logout"),
    path('api/sign_up', views.ApiSignUp.as_view(), name='api_sign_up'),
    path('api/sign_in', views.ApiSignIn.as_view(), name='api_sign_in'),
    path('api/logout', views.ApiLogout.as_view(), name='api_logout'),
]