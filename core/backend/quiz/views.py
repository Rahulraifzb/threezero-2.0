from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def quiz_list(request):
    return render(request,"quiz-list.html")

def quiz_detail(request,pk=None):
    return render(request,"quiz-detail.html")