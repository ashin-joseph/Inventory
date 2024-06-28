from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from Purchase.models import itemTable, purchaseorderTable, orderitemTable
from Stock.models import stockTable


# def update_stock():
#     oit=orderitemTable.objects.all()
#     st= stockTable.objects.all()
#     stock_dic={}
#     for i in st:
#         if i.st_item.item_name in stock_dic:
#             stock_dic[i.st_item.item_name]+= i.st_quantity
#         else:
#             stock_dic[i.st_item.item_name]=i.st_quantity
#     for i,q in stock_dic.items():
#         it=itemTable.objects.get(item_name=i)
#         stock, created =stockTable.objects.get_or_create(st_item=it)
#         stock.st_quantity = q
#         stock.save()

def stock_list(request):
    st=stockTable.objects.all()
    context= {
        'st':st
    }
    return render(request,"stock/stock_list.html",context)



# def update_stock_qty(request):
#     items = itemTable.objects.all()
#     for i in items:
#         print(i, flush=True)
#         total_qty = orderitemTable.objects.filter(oit_item=i).aggregate(total_qty=Sum('oit_quantity'))['total_qty'] or 0
#         obj = stockTable(st_item=i, st_quantity=total_qty)
#         obj.save()
#         print(total_qty, flush=True)
#     return HttpResponse("stoke updated")
