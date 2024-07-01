from django.shortcuts import render
from django.db.models import Sum
from Stock.models import stockTable

def stock_list(request):
    st=stockTable.objects.all()
    return render(request,"stock/stock_list.html",{'st':st})

