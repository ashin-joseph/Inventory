from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from Core.models import itemTable, priceTable, companyprofileTable
import datetime
import random
from Sales.models import salesorderTable, salesorderItemTable, returnSalesTable, returnsalesItemTable
from User.views import index, trial_failed
from Stock.models import stockTable
from django.contrib import messages
from User.decorators import admin_required, staff_required, admin_staff_required

User = get_user_model()


@admin_staff_required
def sales_order(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    item_data = itemTable.objects.all()
    price_data = priceTable.objects.select_related('pt_item').all()
    stock_data = stockTable.objects.all()
    # stock_data = stockTable.objects.select_related('st_remainingStock').all()
    context = {
        'item_data': item_data,
        'price_data': price_data,
        'stock_data': stock_data,
        'base_template': base_template,
    }
    return render(request, "sales/sales_oder.html", context)


@admin_staff_required
def save_sales_order(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        item_names = request.POST.getlist('item_name[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_prices = request.POST.getlist('item_price[]')
        item_total = request.POST.getlist('item_total[]')

        if item_names:
            low_stock_items = []
            for ite, qty in zip(item_names, item_quantity):
                item_instance = itemTable.objects.get(item_name=ite)
                stock_instance = stockTable.objects.get(st_item=item_instance)
                if int(qty) > stock_instance.st_remainingStock:
                    low_stock_items.append(item_instance.item_name)

            if low_stock_items:
                messages.error(request, f"Low stock for items: {', '.join(low_stock_items)}")
                return redirect(sales_order)

            date_str = datetime.datetime.now().strftime("%Y%m%d")
            random_str = random.randint(99, 9999)
            order_num = f"{date_str}SO{random_str}"
            user_instance = User.objects.get(id=user_id)
            so_obj = salesorderTable(sot_bill_number=order_num, sot_user=user_instance)
            so_obj.save()

            try:
                for ite, qty, pri, tot in zip(item_names, item_quantity, item_prices, item_total):
                    item_instant = itemTable.objects.get(item_name=ite)
                    price_instant = priceTable.objects.get(pt_item=item_instant, pt_sellingPrice=pri)
                    soi_obj = salesorderItemTable(soit_bill_number=so_obj, soit_item=item_instant, soit_quantity=qty,
                                                  soit_price=price_instant, soit_total=tot)
                    soi_obj.save()
                return redirect(sales_order_display, orderId=so_obj.id)
            except priceTable.DoesNotExist:
                return redirect(sales_order)
    return redirect(sales_order)


@admin_staff_required
def sales_order_display(request, orderId):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    s_order = get_object_or_404(salesorderTable, id=orderId)
    so_item = salesorderItemTable.objects.filter(soit_bill_number=s_order)
    company_data = companyprofileTable.objects.get()
    address = company_data.company_address
    number = company_data.company_mobile
    gst = company_data.company_gst

    overall = 0
    for j in so_item:
        overall += j.soit_total

    context = {
        's_order': s_order,
        'so_item': so_item,
        'overall': overall,
        'base_template': base_template,
        'company_data': company_data,
        'address': address,
        'number': number,
        'gst': gst,
    }
    return render(request, "sales/sales_order_display.html", context)


@admin_staff_required
def salesreturn(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    salesOrder_data = salesorderTable.objects.all()
    salesOrder = None
    salesItems = None
    so_id = None
    if request.method == "POST":
        so_id = request.POST.get("salesOrderNum_id")
        user_id = request.POST.get("user_id")
    if so_id:
        salesOrder = get_object_or_404(salesorderTable, id=so_id)
        salesItems = salesorderItemTable.objects.filter(soit_bill_number=salesOrder)
    context = {
        'salesOrder_data': salesOrder_data,
        'salesOrder': salesOrder,
        'salesItems': salesItems,
        'base_template': base_template,
    }

    if request.method == "POST":
        salesOdrNum_id = request.POST.get('salesOrderNum_id')  # Get single value
        item_names = request.POST.getlist('item_name[]')
        item_reason = request.POST.getlist('item_reason[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_price = request.POST.getlist('item_price[]')
        item_tax = request.POST.getlist('item_tax[]')
        item_offer = request.POST.getlist('item_offer[]')
        item_amount = request.POST.getlist('item_amount[]')
        if salesOdrNum_id and item_names:
            date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            Return_order_number = f"{date_Rstr}SR{random_number}"
            try:
                sales_instance = salesorderTable.objects.get(id=salesOdrNum_id)
                user_instance = User.objects.get(id=user_id)
                sales_return_number = returnSalesTable(rst_billNum=Return_order_number, rst_poNum=sales_instance,
                                                       rst_user=user_instance)
                sales_return_number.save()
                for ii, ir, iq, ip, it, io, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax,
                                                      item_offer, item_amount):
                    item_instance_return = itemTable.objects.get(item_name=ii)
                    return_items = returnsalesItemTable(rsit_billNum=sales_return_number,
                                                        rsit_item=item_instance_return, rsit_reason=ir,
                                                        rsit_qty=iq, rsit_price=ip, rsit_tax=it, rsit_offer=io,
                                                        rsit_refundAmount=ia)
                    return_items.save()
                return redirect(salesReturn_display, return_id=sales_return_number.id)
            except salesorderTable.DoesNotExist:
                return redirect(trial_failed)
    return render(request, "sales/sales_return.html", context)


@admin_staff_required
def salesReturn_display(request, return_id):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return_order = get_object_or_404(returnSalesTable, id=return_id)
    return_items = returnsalesItemTable.objects.filter(rsit_billNum=return_order)
    company_data = companyprofileTable.objects.get()
    overall = 0
    for i in return_items:
        overall += i.rsit_refundAmount
    context = {
        'return_order': return_order,
        'return_items': return_items,
        'overall': overall,
        'base_template': base_template,
        'company_data': company_data,
    }
    return render(request, "sales/salesReturn_display.html", context)

def sales_bill(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    sales_data= salesorderTable.objects.all().order_by('sot_date')
    salesReturn_data= returnSalesTable.objects.all().order_by('rst_date')
    salesdate_dic={}
    returnsalesdate_dic={}

    for item in sales_data:
        if item.sot_date not in salesdate_dic:
            salesdate_dic[item.sot_date] = {'bills_pairs': [], 'users': []}
        if item.sot_bill_number and item.id:
            salesdate_dic[item.sot_date]['bills_pairs'].append({'sbill': item.sot_bill_number, 'sid': item.id})
        if item.sot_user:
            salesdate_dic[item.sot_date]['users'].append(item.sot_user)

    for item in salesReturn_data:
        if item.rst_date not in returnsalesdate_dic:
            returnsalesdate_dic[item.rst_date] = {'billsr_pairs': [], 'users': []}
        if item.rst_billNum and item.id:
            returnsalesdate_dic[item.rst_date]['billsr_pairs'].append({'srbill': item.rst_billNum, 'srid': item.id})
        if item.rst_user:
            returnsalesdate_dic[item.rst_date]['users'].append(item.rst_user)

    context={
        'base_template': base_template,
        'salesdate_dic': salesdate_dic,
        'returnsalesdate_dic': returnsalesdate_dic,
    }
    return render(request,"sales/sales_bills.html", context)
def salesBill_display(request, billId):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    company_data = companyprofileTable.objects.get()
    sale_ord = get_object_or_404(salesorderTable, id=billId)
    sale_itm = salesorderItemTable.objects.filter(soit_bill_number=sale_ord)
    sale_Amount = 0
    for j in sale_itm:
        sale_Amount += j.soit_total

    context = {
        'base_template': base_template,
        'sale_ord': sale_ord,
        'sale_itm': sale_itm,
        'sale_Amount': sale_Amount,
        'company_data': company_data,
    }
    return render(request, "sales/salesbill_display.html", context)

def returnBill_display(request, billId):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    company_data = companyprofileTable.objects.get()
    saleret_ord = get_object_or_404(returnSalesTable, id=billId)
    saleret_itm = returnsalesItemTable.objects.filter(rsit_billNum=saleret_ord)
    saleret_Amount = 0
    for j in saleret_itm:
        saleret_Amount += j.rsit_refundAmount

    context = {
        'base_template': base_template,
        'saleret_ord': saleret_ord,
        'saleret_itm': saleret_itm,
        'saleret_Amount': saleret_Amount,
        'company_data': company_data,
    }
    return render(request, "sales/returnbill_display.html", context)