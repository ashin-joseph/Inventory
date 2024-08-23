from django.urls import path
from Sales import views


urlpatterns = [
     path('sales_order/',views.sales_order, name="sales_order"),
     path('save_sales_order/',views.save_sales_order, name="save_sales_order"),
     path('sales_order_display/<int:orderId>/',views.sales_order_display, name="sales_order_display"),
     path('salesreturn/',views.salesreturn, name="salesreturn"),
     path('salesReturn_display/<int:return_id>/',views.salesReturn_display, name="salesReturn_display"),
     path('sales_bill/',views.sales_bill, name="sales_bill"),
     path('salesBill_display/<int:billId>/',views.salesBill_display, name="salesBill_display"),
     path('returnBill_display/<int:billId>/',views.returnBill_display, name="returnBill_display"),
]