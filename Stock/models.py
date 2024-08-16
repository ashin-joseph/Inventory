from django.db import models
from Purchase.models import confirmPurchaseItemTable
from Sales.models import salesorderItemTable,returnsalesItemTable
from Core.models import itemTable
from Damage.models import damageTable


class stockTable(models.Model):
    st_item = models.OneToOneField(itemTable, on_delete=models.CASCADE)
    st_purchasesStock = models.PositiveIntegerField(default=0)
    st_soldStock = models.PositiveIntegerField(default=0)
    st_salesReturnStock = models.PositiveIntegerField(default=0)
    st_damageStock = models.PositiveIntegerField(default=0)
    st_remainingStock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.st_item.item_name}"

    def save(self, *args, **kwargs):
        # Calculate the confirmation purchase stock
        purchase_confirm = confirmPurchaseItemTable.objects.filter(cpit_item=self.st_item)
        total_confirm_purchase = 0
        for cp in purchase_confirm:
            total_confirm_purchase += cp.cpit_qty
        self.st_purchasesStock = total_confirm_purchase

        # # Calculate purchase orders
        # purchase_orders = purchaseorderitemTable.objects.filter(oit_item=self.st_item)
        # total_purchased_stock = 0
        # for i in purchase_orders:
        #     total_purchased_stock += i.oit_quantity
        # self.st_purchaseDirectStock = total_purchased_stock

        # Calculate sales orders
        sales_orders = salesorderItemTable.objects.filter(soit_item=self.st_item)
        total_sold_stock = 0
        for j in sales_orders:
            total_sold_stock += j.soit_quantity
        self.st_soldStock = total_sold_stock

        # Calculate the damage stock
        damage_orders =damageTable.objects.filter(dpt_item=self.st_item)
        total_damage_stock = 0
        for l in damage_orders:
            total_damage_stock += l.dpt_damage_qty
        self.st_damageStock = total_damage_stock

        # Calculate the sales return stock
        sales_return = returnsalesItemTable.objects.filter(rsit_item=self.st_item)
        total_return_sales = 0
        for rp in sales_return:
            total_return_sales += rp.rsit_qty
        self.st_salesReturnStock = total_return_sales

        # Calculate the remaining stock
        self.st_remainingStock = max(self.st_purchasesStock + self.st_salesReturnStock - self.st_soldStock - self.st_damageStock, 0)
        super().save(*args, **kwargs)

