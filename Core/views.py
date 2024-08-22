from django.shortcuts import render, redirect
from Core.models import itemTable, vendorTable, priceTable, companyprofileTable
from User.views import index
from django.contrib import messages
from User.decorators import admin_required, staff_required
import datetime
from User.utils import lowstock_list, daily_salesReport, daily_purchaseReport, daily_profitReport


@admin_required
def company_pg(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'

    if request.method == "POST":
        company_id = request.POST.get('company_id')
        if not company_id:
            messages.error(request, "Invalid operation: Company ID is required.")
            return redirect(company_pg)

        try:
            company = companyprofileTable.objects.get(id=company_id)
        except companyprofileTable.DoesNotExist:
            messages.error(request, "Company not found.")
            return redirect(company_pg)

        company_name = request.POST.get('company_name')
        company_person = request.POST.get('company_person')
        company_email = request.POST.get('company_email')
        company_mobile = request.POST.get('company_mobile')
        company_address = request.POST.get('company_address')
        company_gst = request.POST.get('company_gst')
        company_Purchase_note = request.POST.get('company_Purchase_note')
        company_Sales_note = request.POST.get('company_Sales_note')
        company_threshold_Stock = request.POST.get('company_threshold_Stock')

        # Update the existing company record
        company.company_name = company_name
        company.company_person = company_person
        company.company_email = company_email
        company.company_mobile = company_mobile
        company.company_address = company_address
        company.company_gst = company_gst
        company.company_Purchase_note = company_Purchase_note
        company.company_Sales_note = company_Sales_note
        company.company_threshold_Stock = company_threshold_Stock
        company.save()

        messages.success(request, "Company Details Updated Successfully")
        return redirect(company_pg)

    company_data = companyprofileTable.objects.all()
    context = {
        'company_data': company_data,
        'base_template': base_template,
    }
    return render(request, "core/company.html", context)

@admin_required
def item_pg(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    if request.method == "POST":
        item_id = request.POST.get('itemid')
        item_name = request.POST.get('itemname')
        item_category = request.POST.get('itmecategory')
        item_unit = request.POST.get('itemunit')

        if item_id:
            item = itemTable.objects.get(id=item_id)
            item.item_name = item_name
            item.item_category = item_category
            item.item_unit = item_unit
            item.save()
            messages.warning(request, "Item Updated successfully")
        else:
            itemTable.objects.create(item_name=item_name, item_category=item_category, item_unit=item_unit)
            messages.success(request, "Item Added Successfully")
        return redirect(item_pg)
    item_data = itemTable.objects.all()
    return render(request, "core/item.html", {'item_data': item_data, 'base_template': base_template})

@admin_required
def deleteItem(request, Did):
    itemTable.objects.filter(id=Did).delete()
    messages.error(request, "Item Deleted Successfully")
    return redirect(item_pg)

@admin_required
def vendor_pg(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    if request.method == "POST":
        vendorid = request.POST.get('vendorid')
        shopname = request.POST.get('shopname')
        vendorname = request.POST.get('vendorname')
        location = request.POST.get('location')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        gst = request.POST.get('gst')
        note = request.POST.get('note')
        if vendorid:
            vendor = vendorTable.objects.get(vendor_id=vendorid)
            vendor.vendor_shop_name = shopname
            vendor.vendor_location = location
            vendor.vendor_pin = pin
            vendor.vendor_email = email
            vendor.vendor_name = vendorname
            vendor.vendor_phone = phonenumber
            vendor.vendor_GST = gst
            vendor.vendor_note = note
            vendor.save()
            messages.warning(request, "Vendor Updated successfully")
        else:
            vendorTable.objects.create(vendor_shop_name=shopname, vendor_location=location, vendor_pin=pin,
                                       vendor_email=email,
                                       vendor_name=vendorname, vendor_phone=phonenumber, vendor_GST=gst,
                                       vendor_note=note)
            messages.success(request, "Vendor Added Successfully")
        return redirect(vendor_pg)
    vendor_data = vendorTable.objects.all()
    return render(request, "core/vendor.html", {'vendor_data': vendor_data, 'base_template': base_template})

@admin_required
def deleteVendor(request, Did):
    vendorTable.objects.filter(vendor_id=Did).delete()
    messages.error(request, "Vendor Deleted Successfully")
    return redirect(vendor_pg)

@admin_required
def price_pg(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    if request.method == "POST":
        tax = request.POST.get('tax')
        offer = request.POST.get('offer')
        priceTable.objects.all().update(pt_tax=tax, pt_offer=offer)
        messages.info(request, "Tax/Offer Updated Successfully")
        return redirect(price_pg)
    price_data = priceTable.objects.all()
    return render(request, "core/price.html", {'price_data': price_data, 'base_template': base_template})

@admin_required
def updatePrice(request):
    if request.method == "POST":
        item_ids = request.POST.getlist('id[]')
        selling_prices = request.POST.getlist('sellingprice[]')
        taxes = request.POST.getlist('tax[]')
        offers = request.POST.getlist('offer[]')

        if item_ids:
            for ii, sp, ta, of in zip(item_ids, selling_prices, taxes, offers):
                priceTable.objects.filter(id=ii).update(pt_sellingPrice=sp, pt_tax=ta, pt_offer=of)
                messages.info(request, "Updated Price/Tax/Offer Successfully")
        return redirect(price_pg)
    return redirect(index)
@admin_required
def report(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    current_date= datetime.datetime.today()
    low_stock_list = lowstock_list()
    daily_sales, daily_sales_return = daily_salesReport()
    daily_purchase = daily_purchaseReport()
    daily_profit = daily_profitReport()
    context = {
        'current_date':current_date,
        'base_template': base_template,
        'low_stock_list': low_stock_list,
        'daily_sales': daily_sales,
        'daily_sales_return': daily_sales_return,
        'daily_purchase': daily_purchase,
        'daily_profit': daily_profit,
    }
    return render(request,"core/report.html",context)

