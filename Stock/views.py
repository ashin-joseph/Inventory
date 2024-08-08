from django.shortcuts import render
from django.db.models import Sum
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

