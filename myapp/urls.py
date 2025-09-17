from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name='home_page'),
    path("forum/", views.forum, name="forum"),
    path("profile/", views.my_profile, name="my_profile" ),

    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('dietary-intake/', views.dietary_intake, name='dietary_intake'),
    path('workout/', views.workout, name='workout'),
    path('body-metric/', views.body_metrics, name='body_metric'),

    path("workout-routines/", views.workout_routines, name="workout_routines"),

    path("motivation/", views.motivation, name="motivation"),

    path("nutrition/", views.nutritional_guidance, name="nutritional_guidance"),

    path("badges/", views.my_badges, name="my_badges"),
]