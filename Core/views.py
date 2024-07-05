from django.shortcuts import render, redirect
from Core.models import itemTable, vendorTable, priceTable
from User.views import index


def item_pg(request):
    if request.method=="POST":
        item_id = request.POST.get('itemid')
        item_name= request.POST.get('itemname')
        item_category= request.POST.get('itmecategory')
        item_unit= request.POST.get('itemunit')

        if item_id:
            item=itemTable.objects.get(id=item_id)
            item.item_name = item_name
            item.item_category = item_category
            item.item_unit = item_unit
            item.save()
        else:
            itemTable.objects.create(item_name=item_name,item_category=item_category,item_unit=item_unit)
        return redirect(index)
    item_data = itemTable.objects.all()
    return render(request,"core/item.html",{'item_data':item_data})

def deleteItem(request, Did):
    itemTable.objects.filter(id=Did).delete()
    return redirect(item_pg)

def vendor_pg(request):
    if request.method=="POST":
        vendorid= request.POST.get('vendorid')
        shopname= request.POST.get('shopname')
        vendorname= request.POST.get('vendorname')
        location= request.POST.get('location')
        pin= request.POST.get('pin')
        email= request.POST.get('email')
        phonenumber= request.POST.get('phonenumber')
        gst= request.POST.get('gst')
        note= request.POST.get('note')
        if vendorid:
            vendor=vendorTable.objects.get(vendor_id=vendorid)
            vendor.vendor_shop_name=shopname
            vendor.vendor_location=location
            vendor.vendor_pin=pin
            vendor.vendor_email=email
            vendor.vendor_name=vendorname
            vendor.vendor_phone=phonenumber
            vendor.vendor_GST=gst
            vendor.vendor_note=note
            vendor.save()
        else:
            vendorTable.objects.create(vendor_shop_name=shopname,vendor_location=location,vendor_pin=pin,vendor_email=email,
                                   vendor_name=vendorname,vendor_phone=phonenumber,vendor_GST=gst,vendor_note=note)
        return redirect(index)
    vendor_data= vendorTable.objects.all()
    return render(request,"core/vendor.html",{'vendor_data':vendor_data})

def deleteVendor(request,Did):
    vendorTable.objects.filter(vendor_id=Did).delete()
    return redirect(vendor_pg)

def price_pg(request):
    if request.method=="POST":
        tax=request.POST.get('tax')
        offer=request.POST.get('offer')
        priceTable.objects.all().update(pt_tax=tax,pt_offer=offer)
        return redirect(index)
    price_data= priceTable.objects.all()
    return render(request,"core/price.html",{'price_data':price_data})

def updatePrice(request):
    if request.method == "POST":
        item_ids = request.POST.getlist('id')
        selling_prices = request.POST.getlist('sellingprice[]')
        taxes = request.POST.getlist('tax[]')
        offers = request.POST.getlist('offer[]')

        if item_ids:
            for ii, sp, ta, of in zip(item_ids, selling_prices, taxes, offers):
                priceTable.objects.filter(id=ii).update(pt_sellingPrice=sp, pt_tax=ta, pt_offer=of)
        return redirect(index)
    return redirect(index)
