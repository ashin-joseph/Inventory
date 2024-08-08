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
            if user.role == "Admin":
                return redirect(index)
            elif user.role == "Staff":
                return redirect(staff_index)
            else:
                return redirect(trial_failed)
        else:
            return redirect(logout_user_inv)
    else:
        return render(request, "user/Login.html")


@login_required
def logout_user_inv(request):
    logout(request)
    return redirect(login_user_inv)

@login_required
def index(request):
    if request.user.role == "Admin":
        base_template = 'user/Index.html'
    else:
        base_template = 'user/staff_index.html'
    return render(request, "user/Index.html", {'base_template': base_template, 'user': request.user})
@login_required()
def staff_index(requset):
    return render(requset,"user/staff_index.html")
def trial_success(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_success.html", {'base_template': base_template})
def trial_failed(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_failed.html", {'base_template':base_template})

def sample(request):
    return  render(request,"user/sample.html")

def loginuser1(request):
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
def loginuser2(request):
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




