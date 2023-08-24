from django import forms
from .models import Review  # Import the Review model

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
