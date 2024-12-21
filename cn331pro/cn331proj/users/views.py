from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def login_user(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/subject_list')
        else:
            messages.success(request,("There was an errror logging in, Try again"))
            return redirect('/users/login_user')
    else:
        return  render(request, 'login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now login.")
        return redirect('/users/login_user')
    
    return render(request, 'register.html')