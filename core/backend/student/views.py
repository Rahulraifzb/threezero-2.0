from django.http.response import HttpResponse
from django.shortcuts import render
from core.backend.authentication.decorators import * 
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
@allowed_users(allowed_roles=["student","admin"])
def home(request):
    return render(request,"home.html")