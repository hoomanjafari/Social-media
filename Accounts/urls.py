from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/<int:user_id>/', views.UserProfileDetail.as_view(), name='profile'),
    path('editprofile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', views.PasswordResetDoneView.as_view(), name='reset_done'),
    path('reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset_confirm'),
    path('reset/complete/', views.PasswordResetCompleteView.as_view(), name='reset_complete'),
    path('userpost/<int:user_id>/', views.UserPostCreateView.as_view(), name='user_post'),
    path('editpost/<int:post_id>/<slug:post_slug>/', views.UserPostEditView.as_view(), name='edit_user_post'),
    path('delete/post/<int:post_id>/', views.UserPostDeleteView.as_view(), name='delete_user_post'),
    path('post/detail/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('comment/replay/<int:post_id>/', views.CommentReplayView.as_view(), name='replay_comment'),
]
