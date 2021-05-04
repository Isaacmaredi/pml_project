from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            
            if User.objects.filter(username = username).exists():
                messages.error(request, 'That user name already exists')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists() and  User.objects.exclude(email=''):
                    messages.error(request,'That email is already taken')
                    return redirect('accounts:register')
                else:
                    user = User.objects.create_user(username=username, password=password,email=email,first_name=first_name,last_name=last_name)
                    user.save()
                    messages.success(request,'You are now registered and can log in')
                    return redirect('accounts:login_view')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')      
    else:
        return render (request,'accounts/register.html')
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            context= {
                username:"username"
            }
            messages.success(request, 'You are now logged in')
            
            return redirect('pmlmain:index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login_view')
    else:
        return render(request, 'accounts/login.html')

