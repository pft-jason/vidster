from django.urls import path
from .views import *

urlpatterns = [
    path('', gallery_home, name="gallery_home")
]