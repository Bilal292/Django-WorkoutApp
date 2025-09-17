from django.db import models
from django.contrib.auth.models import User

#----- Progress Tracker Page Models ---------
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=100) 
    duration = models.IntegerField()  
    calories_burned = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.type}"

class DietaryIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=100)  
    food = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.meal_type}"

class BodyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()  # In kg
    height = models.FloatField()  # In cm
    bmi = models.FloatField()
    body_fat_percentage = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.weight} kg"
    
#----- Workout Routines Page Models ---------
class WorkoutCategory(models.Model):
    name = models.CharField(max_length=100) 
    
    def __str__(self): 
        return self.name
    
class WorkoutRoutine(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    difficulty = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    category = models.ForeignKey(WorkoutCategory, related_name="routines", on_delete=models.CASCADE) 
    exercises = models.TextField() 
    
    def __str__(self): 
        return self.name

#----- Motivation Page Models --------t-
class VideoMotivation(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuoteMotivation(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text}" - {self.author if self.author else "Unknown"}'

class TipMotivation(models.Model):
    tip_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tip_text[:50]  # Display first 50 chars
    

#----- Community Post Models ---------
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"
    

#----- Nutrtion Page Models ---------
class FitnessGoal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    
    def __str__(self):
        return self.name

class DietPlan(models.Model):
    goal = models.ForeignKey(FitnessGoal, on_delete=models.CASCADE)
    meal = models.ManyToManyField(Meal)
    daily_calories = models.IntegerField()

    def __str__(self):
        return f"{self.goal.name} Plan"
    
#----- Badges Page Models ---------
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="badges/")
    requirement_type = models.CharField(max_length=50, choices=[('calories', 'Calories Burned'), ('weightlifting', 'WeightLifting Sessions'), ('cardio', 'Cardio Sessions'), ('workout', 'Workout Sessions'), ('streak', 'Streak Sessions')])
    requirement_value = models.IntegerField()  # e.g., 10000 calories, 30 workouts

    def __str__(self):
        return self.name
    
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    progress = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.user.username} - {self.badge.name} ({'Unlocked' if self.unlocked else 'Locked'})"
    