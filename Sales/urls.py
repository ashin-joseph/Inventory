from django.urls import path
from Sales import views


urlpatterns = [
     path('sales_order/',views.sales_order, name="sales_order"),
     path('save_sales_order/',views.save_sales_order, name="save_sales_order"),
     path('sales_order_display/',views.sales_order_display, name="sales_order_display"),
]