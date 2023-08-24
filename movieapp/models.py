import pickle
from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    
    def update_average_rating(self):
        reviews = Review.objects.filter(movie=self)
        total_ratings = len(reviews)
        
        if total_ratings > 0:
            average_rating = sum(review.rating for review in reviews) / total_ratings
            self.average_rating = average_rating
            self.total_ratings = total_ratings
        else:
            self.average_rating = 0
            self.total_ratings = 0
        
        self.save()
    
    def get_recommendations(self):
        # Load the movie recommendations model from the pickle file
        with open('static/movies.pkl', 'rb') as f:
            movie_recommendations_model = pickle.load(f)
        
        # Use the loaded model to get movie recommendations
        recommendations = movie_recommendations_model.get_recommendations_for_movie(self.title)
        return recommendations



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)