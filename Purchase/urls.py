from django.urls import path
from Purchase import views

urlpatterns = [
    path('order/', views.order, name="order"),
    path('order_display/<int:order_id>/', views.order_display, name="order_display"),
    path('purchasereturn/', views.purchasereturn, name="purchasereturn"),
    path('purchaseReturn_display/<int:return_id>/', views.purchaseReturn_display, name="purchaseReturn_display"),
]