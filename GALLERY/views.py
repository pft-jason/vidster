from django.shortcuts import render
from .models import * 

def gallery_home(request):
    media = Media.objects.all()
    
    context = {
        'media': media,
    }
    return render(request, 'GALLERY/gallery_home.html', context)
