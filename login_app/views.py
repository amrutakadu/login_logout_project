from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required                     # Homepage will not be loaded and we will get redirected to login page when user is not authenticated (will redirect to login page as maintioned in settings.py LOGIN_URL = 'login')
def homepage(request):
    """
    Function for redirecting to homepage
    """
    return render(request,"home.html")

def register(request):
    """
    Function for creating new user -- Registering new user using NewUserForm 
    """
    if request.method == "POST":
        # print(request.POST)
        form = NewUserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponse("Successfully registered...")
        else:
            return render(request,"register.html",{"form" : form})   

    else:
        return render(request,"register.html",{"register_form" : NewUserForm()})

def login_user(request):
    """
    Function for user login and authentication using AuthenticationForm
    """
    if request.method == "POST":
        # print(request.POST)                     # <QueryDict: {'csrfmiddlewaretoken': ['WgkgCUU84oJsxoC2lvpaOr89qDoB1Edr4pojXI6qTsceHBPQWp3TszTItCtRPMaC'], 'username': ['amruta'], 'password': ['amu@12345']}>
        form = AuthenticationForm(request, data = request.POST)         # Passing QueryDict (obtained from request.POST) to AuthenticationForm
        
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            passwd = form.cleaned_data.get("password")

            user = authenticate(username = uname, password = passwd)        # If user exists returns User -- authenticate is used to check whether username and password for user are available in database or not
            # print(user)     # OUTPUT returns username of user : amruta      # authenticate authenticates password by using same encryption used while saving password

            if user:
                login(request,user)                              # To maintain session and save data in django_session table in database
                messages.success(request,f"Logged in successfully as {user.username}")
                return redirect("homepage")
            else:
                messages.error(request,"Invalid Credentials")
                return redirect("login")
    
    else:
        return render(request,"login_user.html",{"login_form" : AuthenticationForm()})


def logout_user(request):
    """
    Function to logout user using built-in logout(request) function from django.contrib.auth module/package
    and then redirect to login page
    """
    logout(request)                     # deletes data from django_session table    --  also deletes cookies in browser i.e. in client -- 
                                        # Cookies are at client side i.e. at browser and Session is at server side
    return redirect("login")
