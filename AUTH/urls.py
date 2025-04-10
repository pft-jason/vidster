from django.urls import path
from .views import *

urlpatterns = [
    path('', auth_home, name="auth_home"),
    path('login', email_login, name="email_login"),
    path('signup', email_signup, name="email_signup"),
]
