from django.urls import path
from Stock import views


urlpatterns = [
    path("stock_list/", views.stock_list, name="stock_list"),
    path("stock_staff/", views.stock_s_list, name="stock_staff"),
    path("bill_details/", views.bill_details, name="bill_details"),
]