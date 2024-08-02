from django.urls import path
from User import views


urlpatterns = [
    path('', views.login_user_inv, name="login"),
    path('logout/', views.logout_user_inv, name="logout"),
    path('index/', views.index, name="index"),
    path('trial_success/', views.trial_success, name="trial_success"),
    path('trial_failed/', views.trial_failed, name="trial_failed"),
]