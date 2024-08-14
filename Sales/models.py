from django.db import models
from Core.models import itemTable,priceTable
from User.models import User


class salesorderTable(models.Model):
    sot_bill_number=models.CharField(max_length=20, unique=True)
    sot_date= models.DateField(auto_now_add=True)
    sot_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sot_items=models.ManyToManyField(itemTable, through='salesorderItemTable')

    def __str__(self):
        return f"{self.sot_bill_number} {self.sot_date}"


class salesorderItemTable(models.Model):
    soit_bill_number=models.ForeignKey(salesorderTable, on_delete=models.CASCADE)
    soit_item=models.ForeignKey(itemTable, on_delete=models.CASCADE)
    soit_quantity= models.PositiveIntegerField(null=True, blank=True)
    soit_price= models.ForeignKey(priceTable, on_delete=models.CASCADE)
    soit_total= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.soit_bill_number.sot_bill_number

    def save(self, *args, **kwargs):
        super(salesorderItemTable, self).save(*args, **kwargs)
        self.update_sales_stock_qty()

    def update_sales_stock_qty(self):
        from Stock.models import stockTable
        total_sales_quantity=salesorderItemTable.objects.filter(soit_item=self.soit_item).aggregate(total=models.Sum('soit_quantity'))['total']
        sales_stock_item, created = stockTable.objects.get_or_create(st_item=self.soit_item)
        sales_stock_item.st_soldStock = total_sales_quantity
        sales_stock_item.save()

class returnSalesTable(models.Model):
    rst_billNum = models.CharField(max_length=20, unique=True)
    rst_poNum=models.ForeignKey(salesorderTable, on_delete=models.CASCADE)
    rst_date = models.DateTimeField(auto_now_add=True)
    rst_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rst_item = models.ManyToManyField(itemTable, through='returnsalesItemTable')

    def __str__(self):
        return self.rst_billNum


class returnsalesItemTable(models.Model):
    rsit_billNum = models.ForeignKey(returnSalesTable, on_delete=models.CASCADE)
    rsit_item = models.ForeignKey(itemTable, on_delete=models.CASCADE)
    rsit_reason = models.CharField(max_length=100, null=True, blank=True)
    rsit_qty = models.PositiveIntegerField(null=True, blank=True)
    rsit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rsit_tax = models.PositiveIntegerField(null=True, blank=True)
    rsit_offer = models.PositiveIntegerField(null=True, blank=True)
    rsit_refundAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.rsit_billNum.rst_billNum

    def save(self, *args, **kwargs):
        super(returnsalesItemTable, self).save(*args, **kwargs)
        self.update_return_sales_stock_qty()

    def update_return_sales_stock_qty(self):
        from Stock.models import stockTable
        total_quantity = returnsalesItemTable.objects.filter(rsit_item=self.rsit_item).aggregate(total=models.Sum('rsit_qty'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.rsit_item)
        stock_item.st_salesReturnStock = total_quantity
        stock_item.save()