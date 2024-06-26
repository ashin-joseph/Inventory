from django.urls import path
from User import views

urlpatterns = [
    path('', views.login_user_inv, name="login"),
    path('logout/', views.logout_user_inv, name="logout"),
    path('index/', views.index, name="index"),
]