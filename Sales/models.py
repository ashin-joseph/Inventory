from django.db import models
from Purchase.models import itemTable


class priceTable(models.Model):
    pt_item= models.OneToOneField(itemTable, on_delete=models.CASCADE)
    pt_sellingPrice= models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, default=0)
    pt_tax= models.PositiveIntegerField(null=True, blank=True, default=10)
    pt_offer=models.PositiveIntegerField(null=True, blank=True, default=10)
    pt_timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pt_item.item_name


class salesorderTable(models.Model):
    sot_bill_number=models.CharField(max_length=20, unique=True)
    sot_date= models.DateField(auto_now_add=True)
    sot_items=models.ManyToManyField(itemTable, through='salesorderItemTable')

    def __str__(self):
        return f"{self.sot_bill_number} {self.sot_date}"


class salesorderItemTable(models.Model):
    soit_bill_number=models.ForeignKey(salesorderTable, on_delete=models.DO_NOTHING)
    soit_item=models.ForeignKey(itemTable, on_delete=models.DO_NOTHING)
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