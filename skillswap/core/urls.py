from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('post-skill/', views.post_skill, name='post_skill'),
    path('messages/<int:user_id>/', views.message_view, name='messages'),
    path('review/', views.leave_review, name='leave_review'),
    path('matches/', views.match_list, name='matches'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('messages/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('agreements/create/', views.create_agreement, name='create_agreement'),
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html'
    ), name='password_reset'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('edit-skill/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skill-delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),




]
