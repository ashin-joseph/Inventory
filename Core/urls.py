from django.urls import path
from Core import views


urlpatterns = [
    path('item_pg/',views.item_pg, name="item_pg"),
    path('vendor_pg/',views.vendor_pg, name="vendor_pg"),
    path('price_pg/',views.price_pg, name="price_pg"),
]