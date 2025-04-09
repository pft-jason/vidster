from django.shortcuts import render

def gallery_home(request):
    return render(request, 'GALLERY/gallery_home.html')
