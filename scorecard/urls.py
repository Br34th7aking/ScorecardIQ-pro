from django.urls import path
from .views import *

urlpatterns = [
    path('teams/', Teams.as_view()),
    path('venues/', Venues.as_view()),
]
