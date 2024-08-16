from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from Core.models import vendorTable, itemTable
from Purchase.models import orderTable, orderitemsTable, confirmPurchaseTable, confirmPurchaseItemTable
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
        if vendor_id and item_names:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            order_number = f"{date_str}PL{random_number}"
            try:
                vendor_instance = vendorTable.objects.get(vendor_id=vendor_id)
                user_instance = User.objects.get(id=user_id)
                purchase_number = orderTable(ot_order_number=order_number, ot_vendor=vendor_instance,
                                             ot_user=user_instance)
                purchase_number.save()  # save vendor and order
                for name, quantity in zip(item_names, item_quantity):
                    item_instance = itemTable.objects.get(item_name=name)
                    order_item = orderitemsTable(oit_orderNum=purchase_number, oit_items=item_instance,
                                                 oit_quantities=quantity)
                    order_item.save()  # save items
                return redirect(order_display, order_id=purchase_number.id)
                # Redirect to order_display with the new order ID
            except vendorTable.DoesNotExist:
                return redirect(index)
    context = {
        'vendor_data': vendor_data,
        'item_data': item_data,
        'base_template': base_template,
    }
    return render(request, "purchase/Order.html", context)


@admin_required
def order_display(request, order_id):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    order = get_object_or_404(orderTable, id=order_id)
    items = orderitemsTable.objects.filter(oit_orderNum=order)

    context = {
        'order': order,
        'items': items,
        'base_template': base_template,
    }
    return render(request, 'purchase/order_display.html', context)


def confirmpurchase(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    purchaseOrder_data = orderTable.objects.all()
    purchaseOrder = None
    purchaseItems = None
    po_id = None
    if request.method == "POST":
        po_id = request.POST.get("purchaseOrderNum_id")
        user_id = request.POST.get("user_id")
        vendor_id = request.POST.get("vendor_id")
    if po_id:
        purchaseOrder = get_object_or_404(orderTable, id=po_id)
        purchaseItems = orderitemsTable.objects.filter(oit_orderNum=purchaseOrder)
    context = {
        'purchaseOrder_data': purchaseOrder_data,
        'purchaseOrder': purchaseOrder,
        'purchaseItems': purchaseItems,
        'base_template': base_template,
    }

    if request.method == "POST":
        purchaseOdrNum_id = request.POST.get('purchaseOrderNum_id')  # Get single value
        item_names = request.POST.getlist('item_name[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_price = request.POST.getlist('item_price[]')
        item_tax = request.POST.getlist('item_tax[]')
        item_amount = request.POST.getlist('item_amount[]')
        if purchaseOdrNum_id and item_names:
            date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
            random_number = random.randint(100, 999)
            Confirm_order_number = f"{date_Rstr}PC{random_number}"
            try:
                purchase_instance = orderTable.objects.get(id=purchaseOdrNum_id)
                user_instance = User.objects.get(id=user_id)
                vendor_instance = vendorTable.objects.get(vendor_id=vendor_id)
                purchase_number = confirmPurchaseTable(cpt_billNum=Confirm_order_number, cpt_poNum=purchase_instance,
                                                       cpt_vendor=vendor_instance, cpt_user=user_instance)
                purchase_number.save()
                for ii, iq, ip, it, ia in zip(item_names, item_quantity, item_price, item_tax, item_amount):
                    item_instance_return = itemTable.objects.get(item_name=ii)
                    confirm_items = confirmPurchaseItemTable(cpit_billNum=purchase_number,
                                                             cpit_item=item_instance_return,
                                                             cpit_qty=iq, cpit_price=ip, cpit_tax=it, cpit_Amount=ia)
                    confirm_items.save()
                return redirect(confirmpurchase_display, confirm_id=purchase_number.id)
            except orderTable.DoesNotExist:
                return redirect(trial_failed)
    return render(request, "purchase/confirmpurchase_order.html", context)


@admin_required
def confirmpurchase_display(request, confirm_id):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    confirm_order = get_object_or_404(confirmPurchaseTable, id=confirm_id)
    confirm_items = confirmPurchaseItemTable.objects.filter(cpit_billNum=confirm_order)
    overall = 0
    for i in confirm_items:
        price = i.cpit_price * i.cpit_qty
        tax = int((i.cpit_tax / 100)) * price
        total = price + tax
        overall += total
    context = {
        'confirm_order': confirm_order,
        'confirm_items': confirm_items,
        'overall': overall,
        'base_template': base_template,
    }
    return render(request, "purchase/confirmPurchase_display.html", context)

# @admin_required
# def purchaseorder1(request):
#     base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
#     vendor_data = vendorTable.objects.all()
#     item_data = itemTable.objects.all()
#
#
#     if request.method == "POST":
#         user_id = request.POST.get("user_id")
#         vendor_id = request.POST.get("vendor_id")
#         item_names = request.POST.getlist('item_name[]')
#         item_quantity = request.POST.getlist('item_quantity[]')
#         item_prices = request.POST.getlist('item_price[]')
#         item_taxes = request.POST.getlist('item_tax[]')
#         item_total = request.POST.getlist('item_total[]')
#
#         if vendor_id and item_names:
#             date_str = datetime.datetime.now().strftime("%Y%m%d")
#             random_number = random.randint(100, 999)
#             order_number = f"{date_str}PO{random_number}"
#
#             try:
#                 vendor_instance = vendorTable.objects.get(vendor_id=vendor_id)
#                 user_instance = User.objects.get(id=user_id)
#                 purchase_number = purchaseorderTable(pot_order_number=order_number, pot_vendor=vendor_instance, pot_user=user_instance)
#                 purchase_number.save()  # save vendor and order
#
#                 for name, quantity, price, tax, total in zip(item_names, item_quantity, item_prices, item_taxes, item_total):
#                     item_instance = itemTable.objects.get(item_name=name)
#                     order_item = purchaseorderitemTable(oit_purchase_order=purchase_number, oit_item=item_instance,
#                                                 oit_quantity=quantity, oit_price=price, oit_tax_percentage=tax,
#                                                 oit_totalprice=total)
#                     order_item.save()  # save items
#
#                 return redirect(purchaseorder_display,order_id=purchase_number.id)
#                 # Redirect to order_display with the new order ID
#             except vendorTable.DoesNotExist:
#                 return redirect(index)
#
#     return render(request, "purchase/purchase_order.html",
#                   {'vendor_data': vendor_data, 'item_data': item_data, 'base_template': base_template})
# @admin_required
# def purchaseorder_display1(request, order_id):
#     base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
#     order = get_object_or_404(purchaseorderTable, id=order_id)
#     items = purchaseorderitemTable.objects.filter(oit_purchase_order=order)
#
#     overall = 0
#     for i in items:
#         price = i.oit_price * i.oit_quantity
#         tax = int((i.oit_tax_percentage / 100)) * price
#         total = price + tax
#         overall += total
#
#     context = {
#         'order': order,
#         'items': items,
#         'overall': overall,
#         'base_template':base_template,
#     }
#     return render(request, 'purchase/purchaseOrder_display.html', context)
# @admin_required
# def purchasereturn1(request):
#     base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
#     purchaseOrder_data= purchaseorderTable.objects.all()
#     purchaseOrder=None
#     purchaseItems=None
#     po_id= None
#     if request.method=="POST":
#         po_id=request.POST.get("purchaseOrderNum_id")
#         user_id = request.POST.get("user_id")
#     if po_id:
#         purchaseOrder = get_object_or_404(purchaseorderTable, id=po_id)
#         purchaseItems = purchaseorderitemTable.objects.filter(oit_purchase_order=purchaseOrder)
#     context = {
#         'purchaseOrder_data': purchaseOrder_data,
#         'purchaseOrder': purchaseOrder,
#         'purchaseItems': purchaseItems,
#         'base_template' : base_template,
#     }
#
#     if request.method == "POST":
#         purchaseOdrNum_id = request.POST.get('purchaseOrderNum_id')  # Get single value
#         item_names = request.POST.getlist('item_name[]')
#         item_reason = request.POST.getlist('item_reason[]')
#         item_quantity = request.POST.getlist('item_quantity[]')
#         item_price = request.POST.getlist('item_price[]')
#         item_tax = request.POST.getlist('item_tax[]')
#         item_amount = request.POST.getlist('item_amount[]')
#         if purchaseOdrNum_id and item_names:
#             date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
#             random_number = random.randint(100, 999)
#             Return_order_number = f"{date_Rstr}PR{random_number}"
#             try:
#                 purchase_instance = purchaseorderTable.objects.get(id=purchaseOdrNum_id)
#                 user_instance = User.objects.get(id=user_id)
#                 purchase_return_number = returnPurchaseTable(rpt_billNum=Return_order_number, rpt_poNum=purchase_instance,rpt_user=user_instance)
#                 purchase_return_number.save()
#                 for ii, ir, iq, ip, it, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax, item_amount):
#                     item_instance_return = itemTable.objects.get(item_name=ii)
#                     return_items = returnItemTable(rit_billNum=purchase_return_number, rit_item=item_instance_return, rit_reason=ir,
#                                                rit_qty=iq, rit_price=ip, rit_tax=it, rit_refundAmount=ia)
#                     return_items.save()
#                 return redirect(purchaseReturn_display, return_id=purchase_return_number.id)
#             except purchaseorderTable.DoesNotExist:
#                 return redirect(trial_failed)
#     return render(request,"purchase/purchase_return.html", context)
# @admin_required
# def purchaseReturn_display1(request, return_id):
#     base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
#     return_order= get_object_or_404(returnPurchaseTable, id=return_id)
#     return_items= returnItemTable.objects.filter(rit_billNum=return_order)
#     overall=0
#     for i in return_items:
#         price = i.rit_price * i.rit_qty
#         tax = int((i.rit_tax/100))*price
#         total= price+tax
#         overall += total
#     context={
#         'return_order':return_order,
#         'return_items':return_items,
#         'overall':overall,
#         'base_template' : base_template,
#     }
#     return render(request,"purchase/purchaseReturn_display.html", context)
# def purchaseReturnsave1(request):
#     if request.method == "POST":
#         purchaseOdrNum_id = request.POST.get('purchaseOrderNum_id')  # Get single value
#         item_names = request.POST.getlist('item_name[]')
#         item_reason = request.POST.getlist('item_reason[]')
#         item_quantity = request.POST.getlist('item_quantity[]')
#         item_price = request.POST.getlist('item_price[]')
#         item_tax = request.POST.getlist('item_tax[]')
#         item_amount = request.POST.getlist('item_amount[]')
#         if purchaseOdrNum_id and item_names:
#             date_Rstr = datetime.datetime.now().strftime("%Y%m%d")
#             random_number = random.randint(100, 999)
#             Return_order_number = f"{date_Rstr}RO{random_number}"
#             try:
#                 purchase_instance = purchaseorderTable.objects.get(id=purchaseOdrNum_id)
#                 purchase_return_number = returnPurchaseTable(rpt_billNum=Return_order_number, rpt_poNum=purchase_instance)
#                 purchase_return_number.save()
#                 for ii, ir, iq, ip, it, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax, item_amount):
#                     item_instance_return = itemTable.objects.get(item_name=ii)
#                     return_items = returnItemTable(rit_billNum=purchase_return_number, rit_item=item_instance_return, rit_reason=ir,
#                                                rit_qty=iq, rit_price=ip, rit_tax=it, rit_refundAmount=ia)
#                     return_items.save()
#                 return redirect(trial_failed)
#             except purchaseorderTable.DoesNotExist:
#                 return redirect(trial_failed)
#     return redirect(purchasereturn)
