from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_user_inv(request):
    if request.method == "POST":
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        user = authenticate(request, username=login_username, password=login_password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(index)
        else:
            return redirect(logout_user_inv)
    else:
        return render(request, "user/Login.html")
def logout_user_inv(request):
    logout(request)
    return redirect(login_user_inv)


@login_required
def index(request):
    return render(request, "user/Index.html")
