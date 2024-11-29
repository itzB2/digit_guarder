from django.urls import path

from . import views

urlpatterns = [
    path("passwords/", views.passwords),
    path("user_created/", views.user_created)
]