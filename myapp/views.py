from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, DietaryIntakeForm, WorkoutForm, BodyMetricsForm, PostForm, CommentForm
from .models import DietaryIntake, Workout, BodyMetrics, WorkoutCategory, WorkoutRoutine, VideoMotivation, QuoteMotivation, TipMotivation, Post, Comment, FitnessGoal, DietPlan, UserBadge, Badge
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib import messages

def homepage(request):
    return render(request, 'homepage.html')

@login_required(login_url="login")
def my_profile(request):
    user = request.user
    today = now().date()

    # Workout Stats
    total_workouts = Workout.objects.filter(user=user).count()
    recent_workout = Workout.objects.filter(user=user).order_by('-date').first()
    calories_burned = Workout.objects.filter(user=user).aggregate(total=Sum('calories_burned'))['total'] or 0

    # Badge Stats
    unlocked_badges = UserBadge.objects.filter(user=user, unlocked=True)
    locked_badges = UserBadge.objects.filter(user=user, unlocked=False)

    # Dietary Stats for Today
    dietary_today = DietaryIntake.objects.filter(user=user, date=today).aggregate(
        total_calories=Sum('calories') or 0,
        total_protein=Sum('protein') or 0,
        total_carbs=Sum('carbs') or 0
    )

    # Body Metrics (most recent)
    recent_body_metrics = BodyMetrics.objects.filter(user=user).order_by('-date').first()

    # Posts
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else []

    context = {
        'user_posts': user_posts,
        'total_workouts': total_workouts,
        'recent_workout': recent_workout,
        'calories_burned': calories_burned,
        'unlocked_badges': unlocked_badges,
        'locked_badges': locked_badges,
        'dietary_today': dietary_today,
        'recent_body_metrics': recent_body_metrics
    }
    
    return render(request, 'my_profile.html', context)

# ---- USER ACCOUNT VIEWS ----
def register(request):
    if request.user.is_authenticated:
        return redirect('post_list') 
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home_page') 

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('home_page') 
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home_page')



# ---- Progress Tracker Views ----
@login_required(login_url="login")
def dietary_intake(request):
    selected_date = request.GET.get('date') 
    if not selected_date:
        from datetime import date
        selected_date = date.today().isoformat() 

    user_intakes = DietaryIntake.objects.filter(user=request.user, date=selected_date)

    if request.method == 'POST':
        form = DietaryIntakeForm(request.POST)
        if form.is_valid():
            dietary_intake = form.save(commit=False)
            dietary_intake.user = request.user 
            dietary_intake.save()
            return redirect(f"{request.path}?date={dietary_intake.date}") 
    else:
        form = DietaryIntakeForm(initial={'date': selected_date}) 

    return render(request, 'progress-tracker/dietary_intake.html', {
        'form': form,
        'user_intakes': user_intakes,
        'selected_date': selected_date
    })

@login_required(login_url="login")
def workout(request):
    selected_date = request.GET.get('date')  
    if not selected_date:
        from datetime import date
        selected_date = date.today().isoformat()

    user_workouts = Workout.objects.filter(user=request.user, date=selected_date)

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user  
            workout.save()
            return redirect(f"{request.path}?date={workout.date}") 
    else:
        form = WorkoutForm(initial={'date': selected_date})  

    return render(request, 'progress-tracker/workout.html', {
        'form': form,
        'user_workouts': user_workouts,
        'selected_date': selected_date
    })

@login_required(login_url="login")
def body_metrics(request):
    selected_date = request.GET.get('date')
    if not selected_date:
        from datetime import date
        selected_date = date.today().isoformat() 

    user_body_metrics = BodyMetrics.objects.filter(user=request.user, date=selected_date)

    if request.method == 'POST':
        form = BodyMetricsForm(request.POST)
        if form.is_valid():
            body_metrics = form.save(commit=False)
            body_metrics.user = request.user  
            body_metrics.save()
            return redirect(f"{request.path}?date={body_metrics.date}")  
    else:
        form = BodyMetricsForm(initial={'date': selected_date})  

    return render(request, 'progress-tracker/body_metrics.html', {
        'form': form,
        'user_body_metrics': user_body_metrics,
        'selected_date': selected_date
    })


# ---- Workout Routines Views ----
def workout_routines(request):
    category_id = request.GET.get("category", "")  
    difficulty = request.GET.get("difficulty", "")

    categories = WorkoutCategory.objects.all()

    # Filter workouts based on user selections
    workouts = WorkoutRoutine.objects.all() 
    if category_id: # Filter by category
        workouts = workouts.filter(category_id=category_id) 
    if difficulty: # Filter by difficulty level
        workouts = workouts.filter(difficulty=difficulty) 

    return render(request, "workout_routines.html", {
        "workouts": workouts, 
        "categories": categories, 
        "selected_category": category_id, 
        "selected_difficulty": difficulty, 
    })
    

# ---- Motivation Views ----
def motivation(request):
    category = request.GET.get("category", "videos")  # Default to 'videos'

    if category == "videos":
        motivation_content = VideoMotivation.objects.all()
    elif category == "quotes":
        motivation_content = QuoteMotivation.objects.all()
    elif category == "tips":
        motivation_content = TipMotivation.objects.all()
    else:
        motivation_content = []

    return render(request, "motivation.html", {
        "motivation_content": motivation_content,
        "selected_category": category,
    })


# ---- Community Forum Views ----
def forum(request):
    filter_type = request.GET.get("filter", "recent")
    if filter_type == "popular":
        posts = Post.objects.all().order_by('-likes')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, "forum.html", {"posts": posts, "filter_type": filter_type})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()

    return render(request, "forum/post_detail.html", {"post": post, "comments": comments, "comment_form": comment_form})

@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "forum/create_post.html", {"form": form})

@login_required(login_url="login")
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("post_detail", post_id=post.id)
    return redirect("post_detail", post_id=post.id)

@login_required(login_url="login")
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike
    else:
        post.likes.add(request.user)  # Like
    return redirect("post_detail", post_id=post.id)

@login_required(login_url="login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You are not allowed to delete this post.")
    
    return redirect('my_profile')

# ---- Nutrition Views ----
def nutritional_guidance(request):
    goals = FitnessGoal.objects.all()
    selected_goal = request.GET.get("goal")
    
    diet_plans = DietPlan.objects.filter(goal__id=selected_goal) if selected_goal else DietPlan.objects.all()

    return render(request, "nutrition.html", {"goals": goals, "diet_plans": diet_plans})


# ---- Badges Views ----
@login_required(login_url="login")
def my_badges(request):
    user = request.user

    all_badges = Badge.objects.all()

    unlocked_badges = UserBadge.objects.filter(user=user, unlocked=True)

    #Create a list of locked badges
    unlocked_badge_ids = unlocked_badges.values_list('badge_id', flat=True)
    locked_badges = all_badges.exclude(id__in=unlocked_badge_ids)

    return render(request, "my_badges.html", {
        "unlocked_badges": unlocked_badges,
        "locked_badges": locked_badges,
    })
