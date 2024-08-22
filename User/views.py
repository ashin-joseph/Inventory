from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from User.decorators import admin_required, staff_required, admin_staff_required
from .utils import product_details, todays_offer, lowstock_list, user_activity, purchase_overview, sales_overview
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
                return redirect(trial_success)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "user/Login.html")
    else:
        return render(request, "user/Login.html")


@login_required
def logout_user_inv(request):
    logout(request)
    return redirect(login_user_inv)

@login_required
@admin_required
def index(request):
    if request.user.role == "Admin":
        base_template = 'user/Index.html'
    elif request.user.role == "Staff":
        base_template = 'user/staff_index.html'
    else:
        base_template = 'user/trial_success.html'

    low_stock_count, item_count, category_count = product_details()
    sorted_items = todays_offer()
    low_stock_list = lowstock_list()
    active_user_list = user_activity()
    purchaseSum, purchaseNo = purchase_overview()
    salesSum, salesNo, salesReturnSum, salesReturnNo = sales_overview()

    context ={
        'base_template': base_template,

        'user': request.user,

        'low_stock_list': low_stock_list,
        'low_stock_count':low_stock_count,
        'item_count':item_count,
        'category_count':category_count,

        'sorted_items':sorted_items,

        'active_user_list':active_user_list,

        'purchaseSum':purchaseSum,
        'purchaseNo':purchaseNo,

        'salesSum': salesSum,
        'salesNo': purchaseNo,
        'salesReturnSum': salesReturnSum,
        'salesReturnNo': salesReturnNo,

    }
    return render(request, "user/Index.html", context)
@login_required()
@staff_required
def staff_index(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    low_stock_count, item_count, category_count = product_details()
    sorted_items = todays_offer()
    low_stock_list = lowstock_list()
    context = {
        'base_template': base_template,

        'user': request.user,

        'low_stock_list': low_stock_list,
        'low_stock_count': low_stock_count,
        'item_count': item_count,
        'category_count': category_count,

        'sorted_items': sorted_items,
    }
    return render(request,"user/staff_index.html", context)
def trial_success(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_success.html", {'base_template': base_template})
def trial_failed(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_failed.html", {'base_template':base_template})


def sample(request):
    return render(request,"user/sample.html")


# def loginuser1(request):
#     if request.method == "POST":
#         login_username = request.POST.get('login_username')
#         login_password = request.POST.get('login_password')
#         user = authenticate(request, username=login_username, password=login_password)
#         if user is not None and user.is_active:
#             login(request, user)
#             return redirect(index)
#         else:
#             return redirect(logout_user_inv)
#     else:
#         return render(request, "user/Login.html")




