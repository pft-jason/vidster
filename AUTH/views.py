from django.shortcuts import render

def auth_home(request):
    return render(request, 'AUTH/auth_home.html')
