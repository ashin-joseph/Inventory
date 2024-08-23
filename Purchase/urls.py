from django.urls import path
from Purchase import views

urlpatterns = [
    path('order/', views.order, name="order"),
    path('order_display/<int:order_id>/', views.order_display, name="order_display"),
    path('confirmpurchase/', views.confirmpurchase, name="confirmpurchase"),
    path('confirmpurchase_display/<int:confirm_id>/', views.confirmpurchase_display, name="confirmpurchase_display"),
    path('purchase_bill/', views.purchase_bill, name="purchase_bill"),


    # path('purchaseorder/', views.purchaseorder, name="purchaseorder"),
    # path('purchaseorder_display/<int:order_id>/', views.purchaseorder_display, name="purchaseorder_display"),
    # path('purchasereturn/', views.purchasereturn, name="purchasereturn"),
    # path('purchaseReturn_display/<int:return_id>/', views.purchaseReturn_display, name="purchaseReturn_display"),
]