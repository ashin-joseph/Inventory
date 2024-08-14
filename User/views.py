from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from Stock.models import stockTable
from Core.models import itemTable
from Core.models import priceTable
from .models import User
from Purchase.models import orderitemTable, returnItemTable
from Sales.models import salesorderItemTable, returnsalesItemTable
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
                return redirect(trial_success)
        else:
            return redirect(logout_user_inv)
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
    purchaseSum, purchaseNo, purchaseReturnSum, purchaseReturnNo = purchase_overview()
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
        'purchaseReturnSum':purchaseReturnSum,
        'purchaseReturnNo':purchaseReturnNo,

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

def product_details():
    stockdata =stockTable.objects.all()
    itemdata =itemTable.objects.all()
    stockappendNo=[]
    itemappendName=[]
    itemappendCategory=[]
    for i in itemdata:
        itemappendCategory.append(i.item_category)
        itemappendName.append(i.item_name)
    for i in stockdata:
        if i.st_remainingStock < 10:
            stockappendNo.append(i.st_item.item_name)
    return len(stockappendNo),len(itemappendName), len(set(itemappendCategory))


def todays_offer():
    price_data = priceTable.objects.all()
    offer_list = []
    for i in price_data:
        if i.pt_sellingPrice and i.pt_tax and i.pt_offer:
            try:
                selling_price = Decimal(i.pt_sellingPrice)
                tax = (Decimal(i.pt_tax) / 100) * selling_price
                offer = (Decimal(i.pt_offer) / 100) * selling_price
                offer_amount = selling_price + tax - offer
                i.calculated_price = int(offer_amount)
                # Append the item and its calculated offer amount to the list
                offer_list.append((offer, i))
            except (ValueError, Decimal.InvalidOperation) as e:
                continue
    # Sort the list by offer amount in descending order
    offer_list.sort(reverse=True, key=lambda x: x[0])
    # Extract only the sorted items
    sorted_items = [item for _, item in offer_list]
    return sorted_items

def lowstock_list():
    stockdata= stockTable.objects.all()
    stockappendList=[]
    for i in stockdata:
        if i.st_remainingStock < 10:
            stockappendList.append((i.st_item.item_name,i.st_remainingStock))
    return stockappendList

def user_activity():
    userdata = User.objects.all()
    userlist=[]
    for i in userdata:
        userlist.append((i.username, i.last_login, i.email, i.role, i.is_active))
    return userlist

def purchase_overview():
    product_data = orderitemTable.objects.all()
    productReturn_data = returnItemTable.objects.all()
    purchaseSum=0
    purchaseNo=set()
    purchaseReturnSum = 0
    purchaseReturnNo = set()
    for i in product_data:
        if i.oit_purchase_order:
            purchaseNo.add(i.oit_purchase_order)
        if i.oit_totalprice:
            purchaseSum += float(i.oit_totalprice)

    for j in productReturn_data:
        if j.rit_billNum:
            purchaseReturnNo.add(j.rit_billNum)
        if j.rit_refundAmount:
            purchaseReturnSum += int(j.rit_refundAmount)

    return purchaseSum, len(purchaseNo), purchaseReturnSum, len(purchaseReturnNo)


def sales_overview():
    sales_data = salesorderItemTable.objects.all()
    salesReturn_data = returnsalesItemTable.objects.all()
    salesSum = 0
    salesNo = set()
    salesReturnSum = 0
    salesReturnNo = set()
    for i in sales_data:
        if i.soit_bill_number:
            salesNo.add(i.soit_bill_number)
        if i.soit_total:
            salesSum += int(i.soit_total)

    for j in salesReturn_data:
        if j.rsit_billNum:
            salesReturnNo.add(j.rsit_billNum)
        if j.rsit_refundAmount:
            salesReturnSum += int(j.rsit_refundAmount)

    return salesSum, len(salesNo), salesReturnSum, len(salesReturnNo)


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
def todaysoffer():
    price_data = priceTable.objects.all()
    total_offer_amount=0
    for i in price_data:
        if i.pt_sellingPrice and i.pt_tax and i.pt_offer:
            selling_price = Decimal(i.pt_sellingPrice)
            tax=(Decimal(i.pt_tax/100))*selling_price
            offer=(Decimal(i.pt_offer/100))*selling_price
            offer_amount = selling_price + tax - offer
            total_offer_amount += offer_amount
            i.calculated_price = int(offer_amount)
    return price_data



