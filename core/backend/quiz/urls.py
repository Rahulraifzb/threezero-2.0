from django.urls import path 
from .views import *

urlpatterns = [
    path("quiz/",quiz,name="quiz")
]