from django.shortcuts import render

def auth_home(request):
    return render(request, 'AUTH/auth_home.html')

def email_signup(request):
    return render(request, 'AUTH/email_signup.html')

def email_login(request):
    return render(request, 'AUTH/email_login.html')