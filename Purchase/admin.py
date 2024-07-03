from django.contrib import admin
from Purchase.models import purchaseorderTable, orderitemTable

admin.site.register(purchaseorderTable)
admin.site.register(orderitemTable)