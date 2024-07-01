from django.shortcuts import render, redirect
from Purchase.models import itemTable
import datetime
import random
from Sales.models import priceTable, salesorderTable, salesorderItemTable
from User.views import index


def sales_order(request):
    item_data=itemTable.objects.all()
    price_data= priceTable.objects.select_related('pt_item').all()
    context={
        'item_data':item_data,
        'price_data':price_data,
    }
    return render(request, "sales/sales_oder.html", context)


def save_sales_order(request):
    if request.method == "POST":
        item_names = request.POST.getlist('item_name[]')
        item_quantity = request.POST.getlist('item_quantity[]')
        item_prices = request.POST.getlist('item_price[]')
        item_total = request.POST.getlist('item_total[]')

        if item_names:
            date_str=datetime.datetime.now().strftime("%Y%m%d")
            random_str= random.randint(99,9999)
            order_num=f"{date_str}SO{random_str}"
            so_obj=salesorderTable(sot_bill_number=order_num)
            so_obj.save()

            try:
                for ite, qty, pri, tot in zip(item_names,item_quantity, item_prices, item_total):
                    item_instant=itemTable.objects.get(item_name=ite)
                    price_instant= priceTable.objects.get(pt_item=item_instant, pt_sellingPrice=pri)
                    soi_obj=salesorderItemTable(soit_bill_number=so_obj, soit_item=item_instant, soit_quantity=qty, soit_price=price_instant, soit_total=tot)
                    soi_obj.save()
                return redirect(sales_order_display)
            except priceTable.DoesNotExist:
                return redirect(index)
    return redirect(sales_order)

def sales_order_display(request):
    return render(request,"sales/sales_order_display.html")

