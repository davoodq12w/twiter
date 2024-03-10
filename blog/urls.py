from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path('posts', views.post_list, name="post_list"),
    path('post/<int:id>/', views.post_detail, name="post_detail"),
    path('post/add_post/<int:id>', views.add_post, name="add_post"),
    path('post/add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('login/', views.log_in, name='login'),
    path('search/', views.post_search, name='post_search'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('delete_post/<int:id>/confirmed', views.delete_post_confirmed, name='delete_post_confirmed'),
    path('add_account/', views.add_account, name='add_account'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('profile/<int:id>/edit_profile', views.edit_profile, name='edit_profile'),
    path('profile/<int:id>/edit_profile/delete_account', views.delete_account, name='delete_account'),
    path('profile/<int:id>/edit_profile/delete_account/confirmed', views.delete_account_confirmed,
         name='delete_account_confirmed'),
    path('home_screen', views.home_screen, name='home_screen'),

    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

 ]
