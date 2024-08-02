"""
URL configuration for InventorySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import User.urls
import Core.urls
import Purchase.urls
import Stock.urls
import Sales.urls
import Damage.urls
from User.admin import admin_site


urlpatterns = [
    path('myadmin/', admin_site.urls),
    path('admin/', admin.site.urls),
    path('', include(User.urls)),
    path('Core/', include(Core.urls)),
    path('Purchase/', include(Purchase.urls)),
    path('Stock/', include(Stock.urls)),
    path('Sales/', include(Sales.urls)),
    path('Damage/', include(Damage.urls)),

]
