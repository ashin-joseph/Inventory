from django.db import models


class companyprofileTable(models.Model):
    company_name = models.CharField(max_length=50, unique=True)
    company_person = models.CharField(max_length=50, null=True, blank=True)
    company_email = models.EmailField(max_length=100, unique=True)
    company_mobile = models.CharField(max_length=10, null=True, blank=True)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    company_gst = models.CharField(max_length=20)
    company_threshold_Stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.company_name

class vendorTable(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_shop_name = models.CharField(max_length=100, null=True, blank=True)
    vendor_location = models.CharField(max_length=50, null=True, blank=True)
    vendor_pin = models.CharField(max_length=6, null=True, blank=True)
    vendor_email = models.EmailField(max_length=100, null=True, blank=True)
    vendor_name = models.CharField(max_length=50, null=True, blank=True)
    vendor_phone = models.CharField(max_length=10, null=True, blank=True)
    vendor_GST = models.CharField(max_length=100, null=True, blank=True, unique=True)
    vendor_note = models.TextField()

    def __str__(self):
        return self.vendor_shop_name


class itemTable(models.Model):
    UNIT_CHOICES = [
        ('Kilogram', 'Kg'),
        ('Pieces', 'Pcs'),
    ]
    CATEGORY_CHOICE = [
        ('Vegetables', 'Veg'),
        ('Fruits', 'Fru'),
    ]
    item_code = models.CharField(max_length=50, unique=True)
    item_name = models.CharField(max_length=50, null=True, blank=True, unique=True)
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
    pt_item = models.OneToOneField(itemTable, on_delete=models.CASCADE)
    pt_sellingPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    pt_tax = models.PositiveIntegerField(null=True, blank=True, default=0)
    pt_offer = models.PositiveIntegerField(null=True, blank=True, default=0)
    pt_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pt_item.item_name
