from django.urls import path
from movieapp import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("mymovies/", views.mymovies, name="mymovies"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("registration/", views.registration, name="registration"),
    path('review/<int:movie_id>/', views.review, name='review'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),

]
