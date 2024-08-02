from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not an 'Admin' to view this page, Contact admin.")
    return wrap

def staff_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Staff':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not an 'Staff' to view this page, Contact admin.")
    return wrap


def admin_staff_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Staff' or request.user.role == 'Admin':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Either 'Admin/Staff' only can view the page.")
    return wrap