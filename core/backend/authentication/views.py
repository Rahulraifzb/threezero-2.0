from core.backend.authentication.forms import RegisterationForm,LoginForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
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
                    username = form.cleaned_data.get("username")
                    form.save()
                    messages.success(request,f"{username} Your Account Created Successfully")

                    url = request.GET.get("next",None)
                    return redirect(f'/login/?next={url}') if url else redirect("login")
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
                username = None
                try:
                    username = get_object_or_404(User,email=email).username
                except:
                    username = None
                password = form.cleaned_data.get("password")
                url = request.GET.get("next",None)

                if username:
                    user = authenticate(request,username=username,password=password)

                    if user is not None:
                        login(request,user)
                        return redirect(url) if url else redirect("/")
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


