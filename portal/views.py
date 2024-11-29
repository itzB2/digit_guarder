import json
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .models import UserData
from .seralizers import UserDataSerializer

import requests

from . import utils

@api_view(['POST', 'GET'])
@csrf_exempt
def passwords(request):
    data = JSONParser().parse(request)
    uid = data["uid"]
    user_data, exits = UserData.objects.get_or_create(uid=uid, defaults={"uid":uid, "passwords":{}})

    #Get passwords, respond
    if request.method == "GET":
        serialize = UserDataSerializer(user_data)

        return JsonResponse(serialize.data, status = 200)

    #Push a password onto user data
    if request.method == "POST":
        print(data)
        # site = data["site"]
        # encryptedPassword = data["password"] #Password is sent from the client pre encrypted

        # user_data.passwords[site] = encryptedPassword

        # user_data.save()

        # serialize = UserDataSerializer(user_data)

        return JsonResponse({}, status = 201)

@login_required
def dashboard(request):
    res = requests.get("http://localhost:8000/api/passwords/", data=json.dumps({"uid": request.user.id}))
    
    if res.status_code != 200:
        return HttpResponse("Unknown error occured")
    
    response_json = json.loads(res.text)

    passwords = json.loads(response_json["passwords"])

    print(request.user.password)

    # utils.decryptPassword(passwords, request.user.password)

    return render(request, "dashboard.html", {"password":"pass"})

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