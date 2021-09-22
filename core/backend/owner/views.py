from django.http.response import HttpResponse
from django.shortcuts import render
from core.backend.authentication.decorators import *

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
@admin_only
def home(request):
    return HttpResponse("hello from admin Home")