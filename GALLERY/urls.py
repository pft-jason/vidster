from django.urls import path
from .views import *

urlpatterns = [
    path('', gallery_home, name="gallery_home"),
    path('platforms/', platform_list, name="platform_list"),
    path('api/save-url/', SaveUrlView.as_view(), name='save-url'),
]