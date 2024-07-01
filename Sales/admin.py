from django.contrib import admin
from Sales.models import priceTable, salesorderTable, salesorderItemTable

admin.site.register(priceTable)
admin.site.register(salesorderTable)
admin.site.register(salesorderItemTable)
