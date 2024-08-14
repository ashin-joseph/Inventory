from django.shortcuts import render
from Purchase.models import purchaseorderTable, returnPurchaseTable
from Sales.models import salesorderTable, returnSalesTable
from Stock.models import stockTable
from User.decorators import admin_required, staff_required,admin_staff_required

@admin_required
def stock_list(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    st=stockTable.objects.all()
    return render(request,"stock/stock_list.html",{'st':st, 'base_template':base_template})
@staff_required
def stock_s_list(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    st=stockTable.objects.all()
    return render(request,"stock/stock_s_list.html",{'st':st, 'base_template':base_template})

def bill_details(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    purchasebill_data= purchaseorderTable.objects.all().order_by('pot_date')
    purchaseReturn_data= returnPurchaseTable.objects.all().order_by('rpt_date')
    sales_data= salesorderTable.objects.all().order_by('sot_date')
    salesReturn_data= returnSalesTable.objects.all().order_by('rst_date')

    date_dict = {}
    returndate_dic={}
    salesdate_dic={}
    returnsalesdate_dic={}

    for item in purchasebill_data:
        if item.pot_date not in date_dict:
            date_dict[item.pot_date] = {'bills': [], 'users': []}
        if item.pot_order_number:
            date_dict[item.pot_date]['bills'].append(item.pot_order_number)
        if item.pot_user:
            date_dict[item.pot_date]['users'].append(item.pot_user)

    for item in purchaseReturn_data:
        if item.rpt_date not in returndate_dic:
            returndate_dic[item.rpt_date] = {'bills': [], 'users': []}
        if item.rpt_billNum:
            returndate_dic[item.rpt_date]['bills'].append(item.rpt_billNum)
        if item.rpt_user:
            returndate_dic[item.rpt_date]['users'].append(item.rpt_user)

    for item in sales_data:
        if item.sot_date not in salesdate_dic:
            salesdate_dic[item.sot_date] = {'bills': [], 'users': []}
        if item.sot_bill_number:
            salesdate_dic[item.sot_date]['bills'].append(item.sot_bill_number)
        if item.sot_user:
            salesdate_dic[item.sot_date]['users'].append(item.sot_user)

    for item in salesReturn_data:
        if item.rst_date not in returnsalesdate_dic:
            returnsalesdate_dic[item.rst_date] = {'bills': [], 'users': []}
        if item.rst_billNum:
            returnsalesdate_dic[item.rst_date]['bills'].append(item.rst_billNum)
        if item.rst_user:
            returnsalesdate_dic[item.rst_date]['users'].append(item.rst_user)

    context={
        'base_template': base_template,
        'purchasedate_dict': date_dict,
        'returndate_dic': returndate_dic,
        'salesdate_dic': salesdate_dic,
        'returnsalesdate_dic': returnsalesdate_dic,
    }
    return render(request,"stock/bills.html", context)