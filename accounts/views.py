from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("you logged in!"))
            return redirect('index')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('index')

    else:
        return render(request, 'authentication/login.html', {})

def user_logout(request):
    logout(request)
    messages.success(request, ("You're logged out!"))
    print("Logged out")
    return redirect('index')

def registration(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You just registered!"))
            return redirect('index')
    else:
        form = RegisterUserForm()


    return render(request, 'authentication/registration.html', {'form': form,})