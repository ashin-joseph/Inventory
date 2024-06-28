from django.urls import path
from Stock import views


urlpatterns = [
    path("stock_list/", views.stock_list, name="stock_list"),
]