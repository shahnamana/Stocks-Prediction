from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from register.forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your views here.
def register(response):
    if response.method=="POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(response, username=username, password=password)
            if user is not None:
                
                login(response, user)
                return redirect("/")
            else:
                print("inside else")
                messages.error(response,"Username already exists or password doesn't match criteria. Try again.")
                return HttpResponseRedirect("/register")            
            
        else:
            # print(validate_password(form.cleaned_data.get("password1"), user=None, password_validators=None))
            messages.error(response,"Username already exists or password doesn't match criteria. Try again.")
            return HttpResponseRedirect("/register")
    else:
        form = RegisterForm()
    return render(response,"register/register.html", {"form":form})
def csrf_failure(request, reason=""):
    messages.error(request,"Username already exists or password doesn't match criteria. Try again.")
    return HttpResponseRedirect("/register")
def LogOut(request):
    logout(request)
    return redirect("/")
    