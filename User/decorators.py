from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import render, redirect


def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':
            return function(request, *args, **kwargs)
        else:
            return render(request,"user/trial_failed.html")
    return wrap

def staff_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Staff':
            return function(request, *args, **kwargs)
        else:
            return render(request,"user/trial_failed.html")
    return wrap


def admin_staff_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Staff' or request.user.role == 'Admin':
            return function(request, *args, **kwargs)
        else:
            return render(request, "user/trial_failed.html")
            # return HttpResponseForbidden("Either 'Admin/Staff' only can view the page.")
    return wrap