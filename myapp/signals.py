from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workout, Badge, UserBadge
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta

@receiver(post_save, sender=Workout)
def check_badges(sender, instance, **kwargs):
    user = instance.user

    # Calculate total calories burned
    total_calories = Workout.objects.filter(user=user).aggregate(total=Sum('calories_burned'))['total'] or 0
    
    # Count weight lifting workout sessions 
    weightlifting_count = Workout.objects.filter(user=user, type="Weightlifting").count()

    # Count workout sessions 
    workout_count = Workout.objects.filter(user=user).count()

    # Count cardio sessions 
    cardio_count = Workout.objects.filter(user=user, type="Cardio").count()


    # Calculate workout streak (4 workouts in a 7-day window)
    today = now().date()
    one_week_ago = today - timedelta(days=7)
    
    streak_count = (
        Workout.objects
        .filter(user=user, date__range=[one_week_ago, today])
        .values('date')
        .distinct()
        .count()
    )

    # Check badges
    for badge in Badge.objects.all():
        progress = 0
        if badge.requirement_type == "calories":
            progress = total_calories
        elif badge.requirement_type == "weightlifting":
            progress = weightlifting_count
        elif badge.requirement_type == "cardio":
            progress = cardio_count
        elif badge.requirement_type == "workout":
            print(workout_count)
            progress = workout_count
        elif badge.requirement_type == "streak":
            progress = streak_count

        # Get or create UserBadge
        user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
        user_badge.progress = progress

        # Unlock badge if progress meets requirement
        if progress >= badge.requirement_value:
            user_badge.unlocked = True

        user_badge.save()
