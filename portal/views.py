import json
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

import requests

from . import utils


@login_required
def dashboard(request):
    res = requests.get("http://localhost:8000/api/passwords/", data=json.dumps({"uid": request.user.id}))
    passkey = {}

    if res.status_code != 200:
        return HttpResponse("Unknown error occured")
    
    data = json.loads(res.text)
    if "passwords" in data:
        password_entries = data["passwords"].replace("\'", "\"")
        passkey = utils.decryptPassword(json.loads(password_entries), request.user.password)

    return render(request, "dashboard.html", {"password":request.user.password, "uid":request.user.id,"passwords":passkey, "uname":request.user.username})

def signup(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            return redirect("/")
        else:
            return render(request, "signup.html", {"form": form, "error": "Invalid credentials"})

    return render(request, "signup.html", {"form": form})

def login(request):
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            auth_login(request, user)
            request.session.save()

            return redirect("/")
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid credentials"})
    return render(request, "login.html", {"form": form})

@login_required
def logout(request):
    auth_logout(request)

    return redirect("/")