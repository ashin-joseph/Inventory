from django.db import models



class vendorTable(models.Model):
    vendor_id= models.CharField(max_length=10, primary_key=True)
    vendor_shop_name= models.CharField(max_length=100)
    vendor_location= models.CharField(max_length=50)
    vendor_pin= models.CharField(max_length=6,null=True, blank=True)
    vendor_email= models.EmailField(max_length=100,null=True, blank=True)
    vendor_name= models.CharField(max_length=50)
    vendor_phone= models.CharField(max_length=10)
    vendor_GST=models.CharField(max_length=100)
    vendor_note = models.TextField()

    def __str__(self):
        return (self.vendor_shop_name)

class itemTable(models.Model):
    UNIT_CHOICES = [
        ('Kilogram', 'Kg'),
        ('Pieces', 'Pcs'),
    ]
    CATEGORY_CHOICE = [
        ('Vegetables','Veg'),
        ('Fruits','Fru'),
    ]
    item_name = models.CharField(max_length=50)
    item_category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    item_code = models.CharField(max_length=15)
    item_unit = models.CharField(max_length=15, choices=UNIT_CHOICES)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        from Stock.models import stockTable
        super(itemTable, self).save(*args, **kwargs)
        stockTable.objects.get_or_create(st_item=self)


class purchaseorderTable(models.Model):
    pot_order_number= models.CharField(max_length=20, unique=True)
    pot_date = models.DateField(auto_now_add=True)
    pot_vendor = models.ForeignKey(vendorTable, on_delete=models.CASCADE)
    pot_items = models.ManyToManyField(itemTable, through='orderitemTable')

    def __str__(self):
        return (self.pot_order_number)

class orderitemTable(models.Model):
    oit_purchase_order=models.ForeignKey(purchaseorderTable,on_delete=models.CASCADE)
    oit_item= models.ForeignKey(itemTable, on_delete=models.CASCADE)
    oit_quantity = models.PositiveIntegerField(null=True, blank=True)
    oit_price= models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    oit_tax_percentage=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    oit_totalprice = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return (self.oit_purchase_order)


    def save(self, *args, **kwargs):
        super(orderitemTable, self).save(*args, **kwargs)
        self.update_stock_quantity()

    def update_stock_quantity(self):
        from Stock.models import stockTable
        total_quantity = orderitemTable.objects.filter(oit_item=self.oit_item).aggregate(total=models.Sum('oit_quantity'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.oit_item)
        stock_item.st_quantity = total_quantity
        stock_item.save()
