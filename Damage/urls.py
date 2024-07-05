from django.urls import path
from Damage import views

urlpatterns = [
    path('damage/', views.damage, name='damage'),

]