from django.shortcuts import render
from Core.models import itemTable, vendorTable, priceTable
def item_pg(request):
    item_data= itemTable.objects.all()
    return render(request,"core/item.html",{'item_data':item_data})

def vendor_pg(request):
    vendor_data= vendorTable.objects.all()
    return render(request,"core/vendor.html",{'vendor_data':vendor_data})

def price_pg(request):
    price_data= priceTable.objects.all()
    return render(request,"core/price.html",{'price_data':price_data})