from django.contrib import admin
from Core.models import vendorTable, itemTable, priceTable

admin.site.register(vendorTable)
admin.site.register(itemTable)
admin.site.register(priceTable)
