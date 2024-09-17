from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<slug:slug>/', profile_view, name='profile'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]