from django.http.response import JsonResponse
from core.backend.authentication.forms import *
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = RegisterationForm(request.POST or None)
        if request.method == "POST":
            email = request.POST.get("email")
            user = User.objects.filter(email=email).first()
            if user:
                messages.warning(request,f"An user with this {email} is already exit's")
            else:
                if form.is_valid():
                    user = form.save()
                    username = form.cleaned_data.get("username")
                    password = form.cleaned_data.get("password1")
                    group = Group.objects.get(name="student")
                    user.groups.add(group)
                    messages.success(request,f"{username} Your Account Created Successfully")
                    url = request.GET.get("next",None)
                    
                    new_user = authenticate(request,username=user.username,password=password)
                    if new_user is not None:
                        login(request, new_user)
                    return redirect(url) if url else redirect("/student")
                else:
                    print("Form Errors: -----> ",form.errors)
        context = {
            "form":form,
        }
        return render(request,"register.html",context)

def mylogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                email = form.cleaned_data.get("email")
                user = None
                try:
                    user = get_object_or_404(User,email=email)
                except:
                    user = None
                password = form.cleaned_data.get("password")
                url = request.GET.get("next",None)

                if user:
                    user = authenticate(request,username=user.username,password=password)

                    if user is not None:
                        login(request,user)
                        return redirect(url) if url else redirect("/dashboard") if user.groups.first().name == "admin" else redirect("/student")
                    else:
                        messages.warning(request,f"Provided credentials are not valid")
                        
                else:
                    messages.warning(request,f"An user with this {email} isn't exit's")
        context = {
            "form":form
        }
        return render(request,"login.html",context)
    
def mylogout(request):
    logout(request)
    return redirect("login")

@csrf_exempt
@login_required(login_url="login")
def accounts_settings(request):

    password_change_from =  NewPasswordChangeForm(request.user)
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    social_update_form  = SocialUpdateForm(instance=request.user.profile.social) 
    
    if request.GET.get("tab") == None:
        return redirect(reverse('settings') + '?tab=general-tabs')

    if request.method == "POST":
        tab = request.GET.get("tab")
        if tab == "change-password-tabs":
            password_change_from = NewPasswordChangeForm(request.user,request.POST)
            if password_change_from.is_valid():
                user = password_change_from.save()

                print("/n/n/n user:   ",user)
                update_session_auth_hash(request,user)
                messages.success(request, 'Your password was updated successfully🔥')
            else:
                messages.error(request, 'Please correct the error below.')

        elif tab == "general-tabs":
            user_update_form = UserUpdateForm(request.POST,instance=request.user)
            profile_update_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

            if user_update_form.is_valid() and profile_update_form.is_valid():
                print("/n/n/n/n Form is valid /n/n/n/n")
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, 'Your password was updated successfully🔥')
            else:
                print(user_update_form.errors,profile_update_form.errors)
                messages.error(request, 'Please correct the error below.')
        
        elif tab == "information-tabs":
            profile_update_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

            if profile_update_form.is_valid():
                profile_update_form.save()
                messages.success(request, 'Your password was updated successfully🔥')
            else:
                print(user_update_form.errors,profile_update_form.errors)
                messages.error(request, 'Please correct the error below.')

        elif tab == "social-tabs":
            social_update_form = SocialUpdateForm(request.POST,instance=request.user.profile.social) 
            if social_update_form.is_valid():
                social_update_form.save()
                messages.success(request, 'Your password was updated successfully🔥')
            else:
                print(user_update_form.errors,profile_update_form.errors)
                messages.error(request, 'Please correct the error below.')


    context = {
        "password_change_from":password_change_from,
        "user_update_form":user_update_form,
        "profile_update_form":profile_update_form,
        "social_update_form":social_update_form
    }
    return render(request,"account-settings.html",context)

@csrf_exempt
def update_theme(request):
    data = json.loads(request.body)
    theme = data['theme']
    request.user.profile.theme = theme
    request.user.profile.save()
    print('Request:', theme)
    return JsonResponse('Updated..', safe=False)




