from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from User.decorators import admin_required, staff_required, admin_staff_required
User = get_user_model()



def login_user_inv(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
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
    return render(request, "user/Index.html",{'user':request.user})

def trial_success(request):
    return render(request,"user/trial_success.html")

def trial_failed(request):
    return render(request,"user/trial_failed.html")

def loginuser(request):
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
