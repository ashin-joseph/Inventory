from django.contrib import admin
from Purchase.models import vendorTable, itemTable, purchaseorderTable, orderitemTable

admin.site.register(vendorTable)
admin.site.register(itemTable)
admin.site.register(purchaseorderTable)
admin.site.register(orderitemTable)


