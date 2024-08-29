from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from User.decorators import admin_required, staff_required, admin_staff_required
from Core.models import companyprofileTable
from .utils import (product_details, todays_offer, lowstock_list, user_activity,
                    purchase_overview, sales_overview, daily_salesReport, daily_purchaseReport)

import random
from django.core.mail import EmailMessage
from InventorySystem import settings


User = get_user_model()

def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        organization = request.POST.get('organization')
        otp = request.POST.get('otp')  # Make sure to handle OTP validation
        is_superuser = 'is_superuser' in request.POST
        is_staff = 'is_staff' in request.POST

        if otp != str(request.session.get('otp')):
            messages.error(request, "Invalid OTP.")
            return redirect(register_admin)

        if password != confirm_password:
            messages.error(request, "Your passwords do not match.")
            return redirect(register_admin)  # Ensure the URL name matches your URL configuration

        # if User.objects.filter(username=username).exists():
        #     messages.error(request, "Username already exists.")
        #     return redirect(register_admin)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect(register_admin)

        # Here, add OTP validation if necessary

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role,
            organization=organization,
            is_superuser=is_superuser,
            is_staff=is_staff
        )
        user.save()
        messages.success(request, "You have registered as an Admin")
        return redirect(login_user_inv)

    return render(request, 'user/register_admin.html')


def sample(request):
    otp_num = random.randint(999, 9999)
    if request.method == "POST" and "otp_email" in request.POST:
        otp_email = request.POST.get("otp_email")
        email = EmailMessage(
            'OTP',
            f'An OTP is received from StockSmart OTP:{otp_num}.',
            settings.DEFAULT_FROM_EMAIL,
            [otp_email],

        )
        email.send()
        # Store OTP in session
        request.session['otp'] = otp_num

        messages.success(request, "Please check your inbox for the OTP")
        return redirect(register_admin)

    return render(request, "user/sample.html")

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

    company_data = companyprofileTable.objects.get()
    low_stock_count, item_count, category_count = product_details()
    sorted_items = todays_offer()
    low_stock_list = lowstock_list()
    active_user_list = user_activity()
    purchaseSum, purchaseNo = purchase_overview()
    salesSum, salesNo, salesReturnSum, salesReturnNo = sales_overview()
    daily_purchase = daily_purchaseReport()
    daily_sales, daily_sales_return = daily_salesReport()

    context ={
        'base_template': base_template,

        'company_data': company_data,

        'user': request.user,

        'low_stock_list': low_stock_list,
        'low_stock_count':low_stock_count,
        'item_count':item_count,
        'category_count':category_count,

        'sorted_items':sorted_items,

        'active_user_list':active_user_list,

        'purchaseSum':purchaseSum,
        'purchaseNo':purchaseNo,
        'daily_purchase':daily_purchase,

        'salesSum': salesSum,
        'salesNo': salesNo,
        'salesReturnSum': salesReturnSum,
        'salesReturnNo': salesReturnNo,
        'daily_sales': daily_sales,
        'daily_sales_return': daily_sales_return,

    }
    return render(request, "user/Index.html", context)
@login_required()
@staff_required
def staff_index(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    company_data = companyprofileTable.objects.get()
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

        'company_data': company_data,
    }
    return render(request,"user/staff_index.html", context)
def trial_success(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_success.html", {'base_template': base_template})
def trial_failed(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return render(request,"user/trial_failed.html", {'base_template':base_template})









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




