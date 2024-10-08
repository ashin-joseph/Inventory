from django.urls import path
from Core import views

urlpatterns = [
    path('company_pg/', views.company_pg, name="company_pg"),
    path('staff_pg/', views.staff_pg, name="staff_pg"),
    path('deletestaff/<int:Did>/', views.deletestaff, name="deletestaff"),
    path('item_pg/', views.item_pg, name="item_pg"),
    path('deleteItem/<int:Did>/', views.deleteItem, name="deleteItem"),
    path('vendor_pg/', views.vendor_pg, name="vendor_pg"),
    path('deleteVendor/<int:Did>/', views.deleteVendor, name="deleteVendor"),
    path('price_pg/', views.price_pg, name="price_pg"),
    path('updatePrice/', views.updatePrice, name="updatePrice"),
    path('report/', views.report, name="report"),

]
