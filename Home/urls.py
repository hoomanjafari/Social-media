from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow_user'),
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
]
