from django.contrib import admin
from Sales.models import salesorderTable, salesorderItemTable, returnsalesItemTable, returnSalesTable

admin.site.register(salesorderTable)
admin.site.register(salesorderItemTable)
admin.site.register(returnsalesItemTable)
admin.site.register(returnSalesTable)
