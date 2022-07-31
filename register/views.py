from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate 
from .forms import RegisterForm,UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def register(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        
        return redirect("login")

    else:
    
        form = RegisterForm()

    return render(response,"register.html",{"form":form})


@login_required(login_url= 'login')
def editProfile(request):

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
        
        return redirect("dashboard")

    else:
    
        form = UserUpdateForm()

    return render(request,"edit_profile.html",{"form":form})