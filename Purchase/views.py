from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from Core.models import vendorTable, itemTable
from Purchase.models import purchaseorderTable, orderitemTable,returnPurchaseTable, returnItemTable
import datetime
import random
from User.views import index, trial_failed
from django.contrib import messages
from User.decorators import admin_required, staff_required, admin_staff_required
User = get_user_model()


@admin_required
def order(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    vendor_data = vendorTable.objects.all()
    item_data = itemTable.objects.all()


    if request.method == "POST":
        user_id = request.POST.get("user_id")
        vendor_id = request.POST.get("vendor_id")
        item_names = request.POST.getlist('item_name[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_prices = request.POST.getlist('item_price[]')
        item_taxes = request.POST.getlist('item_tax[]')
        item_total = request.POST.getlist('item_total[]')

        if vendor_id and item_names:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            order_number = f"{date_str}PO{random_number}"

            try:
                vendor_instance = vendorTable.objects.get(vendor_id=vendor_id)
                user_instance = User.objects.get(id=user_id)
                purchase_number = purchaseorderTable(pot_order_number=order_number, pot_vendor=vendor_instance, pot_user=user_instance)
                purchase_number.save()  # save vendor and order

                for name, quantity, price, tax, total in zip(item_names, item_quantity, item_prices, item_taxes, item_total):
                    item_instance = itemTable.objects.get(item_name=name)
                    order_item = orderitemTable(oit_purchase_order=purchase_number, oit_item=item_instance,
                                                oit_quantity=quantity, oit_price=price, oit_tax_percentage=tax,
                                                oit_totalprice=total)
                    order_item.save()  # save items

                return redirect(order_display,order_id=purchase_number.id)
                # Redirect to order_display with the new order ID
            except vendorTable.DoesNotExist:
                return redirect(index)

    return render(request, "purchase/Order.html",
                  {'vendor_data': vendor_data, 'item_data': item_data, 'base_template': base_template})

@admin_required
def order_display(request, order_id):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    order = get_object_or_404(purchaseorderTable, id=order_id)
    items = orderitemTable.objects.filter(oit_purchase_order=order)

    overall = 0
    for i in items:
        price = i.oit_price * i.oit_quantity
        tax = int((i.oit_tax_percentage / 100)) * price
        total = price + tax
        overall += total

    context = {
        'order': order,
        'items': items,
        'overall': overall,
        'base_template':base_template,
    }
    return render(request, 'purchase/order_display.html', context)
@admin_required
def purchasereturn(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    purchaseOrder_data= purchaseorderTable.objects.all()
    purchaseOrder=None
    purchaseItems=None
    po_id= None
    if request.method=="POST":
        po_id=request.POST.get("purchaseOrderNum_id")
        user_id = request.POST.get("user_id")
    if po_id:
        purchaseOrder = get_object_or_404(purchaseorderTable, id=po_id)
        purchaseItems = orderitemTable.objects.filter(oit_purchase_order=purchaseOrder)
    context = {
        'purchaseOrder_data': purchaseOrder_data,
        'purchaseOrder': purchaseOrder,
        'purchaseItems': purchaseItems,
        'base_template' : base_template,
    }

    if request.method == "POST":
        purchaseOdrNum_id = request.POST.get('purchaseOrderNum_id')  # Get single value
        item_names = request.POST.getlist('item_name[]')
        item_reason = request.POST.getlist('item_reason[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_price = request.POST.getlist('item_price[]')
        item_tax = request.POST.getlist('item_tax[]')
        item_amount = request.POST.getlist('item_amount[]')
        if purchaseOdrNum_id and item_names:
            date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            Return_order_number = f"{date_Rstr}PRO{random_number}"
            try:
                purchase_instance = purchaseorderTable.objects.get(id=purchaseOdrNum_id)
                user_instance = User.objects.get(id=user_id)
                purchase_return_number = returnPurchaseTable(rpt_billNum=Return_order_number, rpt_poNum=purchase_instance,rpt_user=user_instance)
                purchase_return_number.save()
                for ii, ir, iq, ip, it, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax, item_amount):
                    item_instance_return = itemTable.objects.get(item_name=ii)
                    return_items = returnItemTable(rit_billNum=purchase_return_number, rit_item=item_instance_return, rit_reason=ir,
                                               rit_qty=iq, rit_price=ip, rit_tax=it, rit_refundAmount=ia)
                    return_items.save()
                return redirect(purchaseReturn_display, return_id=purchase_return_number.id)
            except purchaseorderTable.DoesNotExist:
                return redirect(trial_failed)
    return render(request,"purchase/purchase_return.html", context)
@admin_required
def purchaseReturn_display(request, return_id):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    return_order= get_object_or_404(returnPurchaseTable, id=return_id)
    return_items= returnItemTable.objects.filter(rit_billNum=return_order)
    overall=0
    for i in return_items:
        price = i.rit_price * i.rit_qty
        tax = int((i.rit_tax/100))*price
        total= price+tax
        overall += total
    context={
        'return_order':return_order,
        'return_items':return_items,
        'overall':overall,
        'base_template' : base_template,
    }
    return render(request,"purchase/purchaseReturn_display.html", context)

def purchaseReturnsave1(request):
    if request.method == "POST":
        purchaseOdrNum_id = request.POST.get('purchaseOrderNum_id')  # Get single value
        item_names = request.POST.getlist('item_name[]')
        item_reason = request.POST.getlist('item_reason[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_price = request.POST.getlist('item_price[]')
        item_tax = request.POST.getlist('item_tax[]')
        item_amount = request.POST.getlist('item_amount[]')
        if purchaseOdrNum_id and item_names:
            date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            Return_order_number = f"{date_Rstr}RO{random_number}"
            try:
                purchase_instance = purchaseorderTable.objects.get(id=purchaseOdrNum_id)
                purchase_return_number = returnPurchaseTable(rpt_billNum=Return_order_number, rpt_poNum=purchase_instance)
                purchase_return_number.save()
                for ii, ir, iq, ip, it, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax, item_amount):
                    item_instance_return = itemTable.objects.get(item_name=ii)
                    return_items = returnItemTable(rit_billNum=purchase_return_number, rit_item=item_instance_return, rit_reason=ir,
                                               rit_qty=iq, rit_price=ip, rit_tax=it, rit_refundAmount=ia)
                    return_items.save()
                return redirect(trial_failed)
            except purchaseorderTable.DoesNotExist:
                return redirect(trial_failed)
    return redirect(purchasereturn)

