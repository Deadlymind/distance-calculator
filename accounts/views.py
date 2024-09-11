from django.shortcuts import render, HttpResponse , redirect
from django.views import View
#from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import User

def base(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.username)
    else:
        return redirect('login')


def login(request):
    """
    REGISTER:
        GET CREATE USER FORM
        IF POST:
            GET USERNAME AND PASSWORD
            AUTHENTICATIE THE USERNAME AND PASSWORD
            IF USER FOUND: LOGGED IN THE USER AND REDIRECT TO DASHBOARD
            ELSE: RETURN THE INVALID USER FORM
                
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            redirect_to = request.session.get('redirect_to', None) # IF REDIRECT URL: MARKETED CUSTOMER
            if redirect_to:
                del request.session['redirect_to']
                return redirect(redirect_to)
            else:
                mode = 'sourcing' if user.team == 'sales' else "sales"
                return redirect(f"dashboard")
        else:
            messages.info(request,'Username Or Password is incorrect')
    context={}
    return render(request,'accounts/login.html',context)


def logout(request):
    """
    LOGOUT USER
    """
    dj_logout(request)
    return redirect('accounts:login')


def user_profile(request):
    """
    IF LOGGED IN: RETURN TO PROFILE PAGE
    IF NOT LOGGED IN: RETURN ERROR
    """
    if request.user.is_authenticated:
        context={}
        return render(request, 'accounts/user_profile.html', context)
    else:
        return HttpResponse('please login with your credentials to view user profile page ')


class UserListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        users = User.objects.all().exclude(id=request.user.id)
        return render(request, "accounts/list.html", {
            "users": users
        })

    def post(self, request):
        user = User.objects.get(id=request.POST.get('id'))
        user.is_active = request.POST.get('is_active') == "on"
        if request.POST.get('team') == 'admin':
            user.is_superuser = True
        else:
            user.is_superuser = False
            user.team = request.POST.get('team')
        user.save()

        return redirect('accounts:list')

class UserCreateView(View):

    
    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        users = User.objects.all()
        return render(request, "accounts/create.html", {
            "users": users
        })

    def post(self, request):
        if User.objects.filter(
            username=request.POST.get('username')
        ).exists():
            return render(request, "accounts/create.html", {
                "error": "User with this username already exists"
            })
        else:
            user = User(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
            )
            team = request.POST.get('team')
            if team == 'admin':
                user.is_superuser = True
                user.team = 'sourcing'
            else:
                user.team = team
            user.save()
            user.set_password(request.POST.get('password'))

            return redirect('accounts:list')
