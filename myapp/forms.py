from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import DietaryIntake, Workout, BodyMetrics, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DietaryIntakeForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )

    class Meta:
        model = DietaryIntake
        fields = ['date', 'meal_type', 'food', 'calories', 'protein', 'carbs', 'fat']

class WorkoutForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )

    class Meta:
        model = Workout
        fields = ['date', 'type', 'duration', 'calories_burned']

class BodyMetricsForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )

    class Meta:
        model = BodyMetrics
        fields = ['date', 'weight', 'height', 'bmi', 'body_fat_percentage']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']