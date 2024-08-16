from django.shortcuts import render
from Purchase.models import confirmPurchaseTable
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
    purchaseConfirm_data= confirmPurchaseTable.objects.all().order_by('cpt_date')
    sales_data= salesorderTable.objects.all().order_by('sot_date')
    salesReturn_data= returnSalesTable.objects.all().order_by('rst_date')
    purchaseconfirmdate_dic={}
    salesdate_dic={}
    returnsalesdate_dic={}

    for item in purchaseConfirm_data:
        if item.cpt_date not in purchaseconfirmdate_dic:
            purchaseconfirmdate_dic[item.cpt_date] = {'bills': [], 'users': []}
        if item.cpt_billNum:
            purchaseconfirmdate_dic[item.cpt_date]['bills'].append(item.cpt_billNum)
        if item.cpt_user:
            purchaseconfirmdate_dic[item.cpt_date]['users'].append(item.cpt_user)

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
        'purchaseconfirmdate_dic': purchaseconfirmdate_dic,
        'salesdate_dic': salesdate_dic,
        'returnsalesdate_dic': returnsalesdate_dic,
    }
    return render(request,"stock/bills.html", context)