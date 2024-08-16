from django.contrib import admin
from Purchase.models import orderTable, orderitemsTable, confirmPurchaseTable, confirmPurchaseItemTable

admin.site.register(orderTable)
admin.site.register(orderitemsTable)
admin.site.register(confirmPurchaseTable)
admin.site.register(confirmPurchaseItemTable)