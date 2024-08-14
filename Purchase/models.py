from django.db import models
from decimal import Decimal
from Core.models import vendorTable,itemTable
from User.models import User


class purchaseorderTable(models.Model):
    pot_order_number= models.CharField(max_length=20, unique=True)
    pot_date = models.DateField(auto_now_add=True)
    pot_vendor = models.ForeignKey(vendorTable, on_delete=models.CASCADE)
    pot_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pot_items = models.ManyToManyField(itemTable, through='orderitemTable')

    def __str__(self):
        return (self.pot_order_number)

class orderitemTable(models.Model):
    oit_purchase_order=models.ForeignKey(purchaseorderTable,on_delete=models.CASCADE)
    oit_item= models.ForeignKey(itemTable, on_delete=models.CASCADE)
    oit_quantity = models.PositiveIntegerField(null=True, blank=True)
    oit_price= models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    oit_tax_percentage=models.PositiveIntegerField(null=True, blank=True)
    oit_totalprice = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.oit_purchase_order.pot_order_number} + {self.oit_item.item_name}"

    def save(self, *args, **kwargs):
        super(orderitemTable, self).save(*args, **kwargs)
        self.update_purchase_stock_qty()
        self.update_selling_price()

    def update_purchase_stock_qty(self):
        from Stock.models import stockTable
        total_quantity = orderitemTable.objects.filter(oit_item=self.oit_item).aggregate(total=models.Sum('oit_quantity'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.oit_item)
        stock_item.st_purchasesStock = total_quantity
        stock_item.save()

    def update_selling_price(self):
        from Core.models import priceTable
        price = orderitemTable.objects.filter(oit_item=self.oit_item).aggregate(max_price=models.Max('oit_price'))['max_price']
        price_tax_per = orderitemTable.objects.filter(oit_item=self.oit_item).aggregate(max_tax=models.Max('oit_tax_percentage'))['max_tax']
        price_tax = (Decimal(price_tax_per)/Decimal(100) * Decimal(price))
        price_margin = (Decimal(8)/Decimal(100) * Decimal(price))
        item_price, created = priceTable.objects.get_or_create(pt_item=self.oit_item)
        item_price.pt_sellingPrice = price + price_tax + price_margin
        item_price.save()

class returnPurchaseTable(models.Model):
    rpt_billNum = models.CharField(max_length=20, unique=True)
    rpt_poNum=models.ForeignKey(purchaseorderTable, on_delete=models.CASCADE)
    rpt_date = models.DateTimeField(auto_now_add=True)
    rpt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rpt_item = models.ManyToManyField(itemTable, through='returnItemTable')

    def __str__(self):
        return self.rpt_billNum


class returnItemTable(models.Model):
    rit_billNum = models.ForeignKey(returnPurchaseTable, on_delete=models.CASCADE)
    rit_item = models.ForeignKey(itemTable, on_delete=models.CASCADE)
    rit_reason = models.CharField(max_length=100, null=True, blank=True)
    rit_qty = models.PositiveIntegerField(null=True, blank=True)
    rit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rit_tax = models.PositiveIntegerField(null=True, blank=True)
    rit_refundAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.rit_billNum.rpt_billNum

    def save(self, *args, **kwargs):
        super(returnItemTable, self).save(*args, **kwargs)
        self.update_return_purchase_stock_qty()

    def update_return_purchase_stock_qty(self):
        from Stock.models import stockTable
        total_quantity = returnItemTable.objects.filter(rit_item=self.rit_item).aggregate(total=models.Sum('rit_qty'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.rit_item)
        stock_item.st_purchasesReturnStock = total_quantity
        stock_item.save()