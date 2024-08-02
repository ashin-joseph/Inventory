from django.contrib import admin
from Purchase.models import purchaseorderTable, orderitemTable, returnPurchaseTable, returnItemTable

admin.site.register(purchaseorderTable)
admin.site.register(orderitemTable)
admin.site.register(returnPurchaseTable)
admin.site.register(returnItemTable)