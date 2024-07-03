from django.contrib import admin
from Sales.models import salesorderTable, salesorderItemTable

admin.site.register(salesorderTable)
admin.site.register(salesorderItemTable)
