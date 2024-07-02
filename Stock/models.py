from django.db import models
from Purchase.models import itemTable, orderitemTable
from Sales.models import salesorderItemTable
from Sales.models import priceTable


class stockTable(models.Model):
    st_item = models.OneToOneField(itemTable, on_delete=models.CASCADE)
    st_purchasesStock = models.PositiveIntegerField(default=0)
    st_soldStock = models.PositiveIntegerField(default=0)
    st_remainingStock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.st_item.item_name}"

    def save(self, *args, **kwargs):
        # Calculate the purchased stock from the purchase orders
        purchase_orders = orderitemTable.objects.filter(oit_item=self.st_item)
        total_purchased_stock = 0
        for order in purchase_orders:
            total_purchased_stock += order.oit_quantity
        self.st_purchasesStock = total_purchased_stock

        # Calculate the sold stock from the sales orders
        sales_orders = salesorderItemTable.objects.filter(soit_item=self.st_item)
        total_sold_stock = 0
        for order in sales_orders:
            total_sold_stock += order.soit_quantity
        self.st_soldStock = total_sold_stock

        # Calculate the remaining stock
        self.st_remainingStock = max(self.st_purchasesStock - self.st_soldStock, 0)

        super().save(*args, **kwargs)

