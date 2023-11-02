from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_generic_hello),
    path('hello/', views.say_hello_to_my_little_puppy),
    path('list/', views.list_members),
    path('home/', views.home),
    path('home/title/', views.home_title),
]