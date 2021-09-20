from django.urls import path 
from .views import *

urlpatterns = [
    path("quiz/",quiz_list,name="quiz-list"),
    path("quiz/<str:pk>/",quiz_detail,name="quiz-detail")
]