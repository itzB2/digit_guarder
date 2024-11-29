import json
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

import requests

@login_required
def dashboard(request):
    
    res = requests.post("http://localhost:8000/api/user_created/", data="{{}}")
    # print(res.text)

    return render(request, "dashboard.html")

def login(request):
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            auth_login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid credentials"})
    return render(request, "login.html", {"form": form})

def signup(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            res = requests.post("http://localhost:8000/api/user_created/")
            print(res.status_code)

            return redirect("/")
        else:
            return render(request, "signup.html", {"form": form, "error": "Invalid credentials"})

    return render(request, "signup.html", {"form": form})