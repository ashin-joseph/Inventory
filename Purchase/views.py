from django.shortcuts import render, redirect, get_object_or_404
from Purchase.models import vendorTable, itemTable, purchaseorderTable, orderitemTable
import datetime
import random
from User.views import index


def order(request):
    vendor_data = vendorTable.objects.all()
    item_data = itemTable.objects.all()

    if request.method == "POST":
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
                purchase_number = purchaseorderTable(pot_order_number=order_number, pot_vendor=vendor_instance)
                purchase_number.save()  # save vendor and order

                for name, quantity, price, tax, total in zip(item_names, item_quantity, item_prices, item_taxes, item_total):
                    item_instance = itemTable.objects.get(item_name=name)
                    order_item = orderitemTable(oit_purchase_order=purchase_number, oit_item=item_instance,
                                                oit_quantity=quantity, oit_price=price, oit_tax_percentage=tax,
                                                oit_totalprice=total)
                    order_item.save()  # save items

                return redirect(order_display,
                                order_id=purchase_number.id)  # Redirect to order_display with the new order ID
            except vendorTable.DoesNotExist:
                return redirect(index)

    return render(request, "purchase/Order.html",
                  {'vendor_data': vendor_data, 'item_data': item_data})


def order_display(request, order_id):
    order = get_object_or_404(purchaseorderTable, id=order_id)
    items = orderitemTable.objects.filter(oit_purchase_order=order)

    total_p = []
    overall = 0
    for i in items:
        price = i.oit_price * i.oit_quantity
        tax = (i.oit_tax_percentage / 100) * price
        total = price + tax
        total_p.append(total)
        overall += total

    context = {
        'order': order,
        'items': items,
        'overall': overall,
    }
    return render(request, 'purchase/order_display.html', context)

# def order_details(request, vi_id):
#     po_number=purchaseorder_table.objects.all()
#     order_vendor_data=get_object_or_404(purchaseorder_table, id=vi_id)
#     order_item_data=orderitem_Table.objects.filter(oit_purchase_order=order_vendor_data)
#
#     context = {
#         'po_number': po_number,
#         'order_vendor_data':order_vendor_data,
#         'order_item_data':order_item_data
#     }
#     return render(request,"purchase/order_dis.html",context)
