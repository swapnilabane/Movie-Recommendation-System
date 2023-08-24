from django.shortcuts import render,redirect,get_object_or_404
import requests
import pickle
import pandas as pd
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Movie, Review
from .forms import ReviewForm

with open('static/movies.pkl', 'rb') as file:
    movies = pd.read_pickle(file)

# print(movies.head())


# with open('static/movies.pkl', 'rb') as file:
#     movies = pd.read_pickle(file)


def recommend(movie):
    
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    for i in distances[1:6]:
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name


# Create your views here.
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def mymovies(request):
    status = False  # Initialize the status variable
    recommended_movies = []  # Initialize the recommended movies list

    if request.user.is_authenticated:
        movie_list = movies['title'].values
        if request.method == "POST":
            try:
                if 'movies' in request.POST:
                    selected_movie = request.POST['search']
                    recommended_movies = recommend(selected_movie)
                    status = True  # Update the status variable to True

            except Exception as e:
                error = {'error': e}
                return render(request, "mymovies.html", {
                    'error': error,
                    'movie_list': movie_list,
                    'status': status,
                })

        return render(request, "mymovies.html", {
            'movie_list': movie_list,
            'recommended_movies': recommended_movies,
            'status': status,
        })
    else:
        return redirect('/')




def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/registration')
        else:
            return render(request, "user_login.html")
    


def user_logout(request):
    logout(request)
    return redirect('/')

def registration(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confpassword=request.POST['confirmpassword']
        if password==confpassword:
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            login(request,user)
            return redirect('/')
        else:
            return redirect('/registration')
    else:
        return render(request,"registration.html")


# views.py

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})


def review(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            
            # Update movie's average rating and total ratings
            movie.update_average_rating()
            
            return redirect('/movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    
    return render(request, 'review.html', {'form': form, 'movie': movie})
