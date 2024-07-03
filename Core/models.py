from django.db import models


class vendorTable(models.Model):
    vendor_id= models.AutoField(primary_key=True)
    vendor_shop_name= models.CharField(max_length=100,null=True, blank=True)
    vendor_location= models.CharField(max_length=50,null=True, blank=True)
    vendor_pin= models.CharField(max_length=6,null=True, blank=True)
    vendor_email= models.EmailField(max_length=100,null=True, blank=True)
    vendor_name= models.CharField(max_length=50,null=True, blank=True)
    vendor_phone= models.CharField(max_length=10,null=True, blank=True)
    vendor_GST=models.CharField(max_length=100,null=True, blank=True)
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
    item_name = models.CharField(max_length=50,null=True, blank=True)
    item_category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    item_unit = models.CharField(max_length=15, choices=UNIT_CHOICES)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        from Stock.models import stockTable
        super(itemTable, self).save(*args, **kwargs)
        stockTable.objects.get_or_create(st_item=self)
        priceTable.objects.get_or_create(pt_item=self)

    # def save(self, *args, **kwargs):
    #     from Sales.models import stockTable
    #     super(itemTable, self).save(*args, **kwargs)
    #     stockTable.objects.get_or_create(st_item=self)


class priceTable(models.Model):
    pt_item= models.OneToOneField(itemTable, on_delete=models.DO_NOTHING)
    pt_sellingPrice= models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, default=0)
    pt_tax= models.PositiveIntegerField(null=True, blank=True, default=1)
    pt_offer=models.PositiveIntegerField(null=True, blank=True, default=1)
    pt_timestamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pt_item.item_name