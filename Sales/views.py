from django.shortcuts import render, redirect, get_object_or_404
from Core.models import itemTable, priceTable
import datetime
import random
from Sales.models import salesorderTable, salesorderItemTable, returnSalesTable, returnsalesItemTable
from User.views import index,trial_failed, trial_success
from Stock.models import stockTable
from  django.contrib import messages


def sales_order(request):
    item_data = itemTable.objects.all()
    price_data = priceTable.objects.select_related('pt_item').all()
    stock_data = stockTable.objects.select_related('st_remainingStock').all()
    context = {
        'item_data': item_data,
        'price_data': price_data,
        'stock_data' : stock_data,
    }
    return render(request, "sales/sales_oder.html", context)


def save_sales_order(request):
    if request.method == "POST":
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
            so_obj = salesorderTable(sot_bill_number=order_num)
            so_obj.save()

            try:
                for ite, qty, pri, tot in zip(item_names, item_quantity, item_prices, item_total):
                    item_instant = itemTable.objects.get(item_name=ite)
                    price_instant = priceTable.objects.get(pt_item=item_instant, pt_sellingPrice=pri)
                    soi_obj = salesorderItemTable(soit_bill_number=so_obj, soit_item=item_instant, soit_quantity=qty, soit_price=price_instant, soit_total=tot)
                    soi_obj.save()
                return redirect(sales_order_display, orderId=so_obj.id)
            except priceTable.DoesNotExist:
                return redirect(index)
    return redirect(sales_order)


def sales_order_display(request, orderId):
    s_order = get_object_or_404(salesorderTable, id=orderId)
    so_item = salesorderItemTable.objects.filter(soit_bill_number=s_order)

    overall = 0
    for j in so_item:
        price = j.soit_price.pt_sellingPrice * j.soit_quantity
        tax = int((j.soit_price.pt_tax / 100)) * price
        offer = int((j.soit_price.pt_offer / 100)) * price
        total_s = price + tax - offer
        overall += total_s

    context = {
        's_order': s_order,
        'so_item': so_item,
        'overall': overall
    }
    return render(request, "sales/sales_order_display.html", context)


def salesreturn(request):
    salesOrder_data= salesorderTable.objects.all()
    salesOrder=None
    salesItems=None
    so_id= None
    if request.method=="POST":
        so_id=request.POST.get("salesOrderNum_id")
    if so_id:
        salesOrder = get_object_or_404(salesorderTable, id=so_id)
        salesItems = salesorderItemTable.objects.filter(soit_bill_number=salesOrder)
    context = {
        'salesOrder_data': salesOrder_data,
        'salesOrder': salesOrder,
        'salesItems': salesItems,
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
            Return_order_number = f"{date_Rstr}SRO{random_number}"
            try:
                sales_instance = salesorderTable.objects.get(id=salesOdrNum_id)
                sales_return_number = returnSalesTable(rst_billNum=Return_order_number, rst_poNum=sales_instance)
                sales_return_number.save()
                for ii, ir, iq, ip, it, io, ia in zip(item_names, item_reason, item_quantity, item_price, item_tax, item_offer, item_amount):
                    item_instance_return = itemTable.objects.get(item_name=ii)
                    return_items = returnsalesItemTable(rsit_billNum=sales_return_number, rsit_item=item_instance_return, rsit_reason=ir,
                                               rsit_qty=iq, rsit_price=ip, rsit_tax=it, rsit_offer=io, rsit_refundAmount=ia)
                    return_items.save()
                return redirect(salesReturn_display, return_id=sales_return_number.id)
            except salesorderTable.DoesNotExist:
                return redirect(trial_failed)
    return render(request,"sales/sales_return.html", context)



def salesReturn_display(request, return_id):
    return_order= get_object_or_404(returnSalesTable, id=return_id)
    return_items= returnsalesItemTable.objects.filter(rsit_billNum=return_order)
    overall=0
    for i in return_items:
        price = i.rsit_price * i.rsit_qty
        tax = int((i.rsit_tax/100))*price
        total= price+tax
        overall += total
    context={
        'return_order':return_order,
        'return_items':return_items,
        'overall':overall,
    }
    return render(request,"sales/salesReturn_display.html", context)