from django.db import models
from decimal import Decimal
from Core.models import vendorTable, itemTable
from User.models import User


class orderTable(models.Model):
    ot_order_number= models.CharField(max_length=50, unique=True)
    ot_date = models.DateField(auto_now_add=True)
    ot_vendor = models.ForeignKey(vendorTable, on_delete=models.CASCADE)
    ot_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ot_items = models.ManyToManyField(itemTable, through='orderitemsTable')

    def __str__(self):
        return (self.ot_order_number)

class orderitemsTable(models.Model):
    oit_orderNum=models.ForeignKey(orderTable,on_delete=models.CASCADE)
    oit_items= models.ForeignKey(itemTable, on_delete=models.CASCADE)
    oit_quantities = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.oit_purchase_order.ot_order_number} + {self.oit_item.item_name}"


class confirmPurchaseTable(models.Model):
    cpt_billNum = models.CharField(max_length=50, unique=True)
    cpt_vendor = models.ForeignKey(vendorTable, on_delete=models.CASCADE)
    cpt_date = models.DateField(auto_now_add=True)
    cpt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cpt_item = models.ManyToManyField(itemTable, through='confirmPurchaseItemTable')

    def __str__(self):
        return self.cpt_billNum

    def save(self, *args, **kwargs):
        super(confirmPurchaseTable, self).save(*args, **kwargs)
        # Backup data after all items are saved
        self.backup_purchase_data()

    def backup_purchase_data(self):
        # Create the purchase backup entry only if it doesn't exist
        cpt_b_backup, created = cpt_backup.objects.get_or_create(
            cpt_b_billNum=self.cpt_billNum,
            defaults={
                'cpt_b_vendor': self.cpt_vendor.vendor_shop_name,
                'cpt_b_address': self.cpt_vendor.vendor_location,
                'cpt_b_gst': self.cpt_vendor.vendor_GST,
                'cpt_b_contact': self.cpt_vendor.vendor_name,
                'cpt_b_phone': self.cpt_vendor.vendor_phone,
                'cpt_b_date': str(self.cpt_date),
                'cpt_b_user': self.cpt_user.username
            }
        )
        return cpt_b_backup

    # def delete_after_backup(self):
    #     confirmPurchaseItemTable.objects.filter(cpit_billNum=self).delete()
    #     self.delete()

class confirmPurchaseItemTable(models.Model):
    cpit_billNum = models.ForeignKey(confirmPurchaseTable, on_delete=models.CASCADE)
    cpit_item = models.ForeignKey(itemTable, on_delete=models.CASCADE)
    # cpit_item = models.ForeignKey(itemTable, on_delete=models.SET_NULL, null=True, blank=True)
    cpit_qty = models.PositiveIntegerField(null=True, blank=True)
    cpit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cpit_tax = models.PositiveIntegerField(null=True, blank=True)
    cpit_Amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cpit_billNum.cpt_billNum

    def save(self, *args, **kwargs):
        super(confirmPurchaseItemTable, self).save(*args, **kwargs)
        self.update_confirm_purchase_stock_qty()
        self.update_price()
        # Call backup after saving each item
        self.cpit_billNum.backup_purchase_data()
        self.backup_purchase_item_data()

    def update_confirm_purchase_stock_qty(self):
        from Stock.models import stockTable
        total_quantity = confirmPurchaseItemTable.objects.filter(cpit_item=self.cpit_item).aggregate(total=models.Sum('cpit_qty'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.cpit_item)
        stock_item.st_purchasesStock = total_quantity
        stock_item.save()

    def update_price(self):
        from Core.models import priceTable
        price = confirmPurchaseItemTable.objects.filter(cpit_item=self.cpit_item).aggregate(max_price=models.Max('cpit_price'))['max_price']
        price_tax_per = confirmPurchaseItemTable.objects.filter(cpit_item=self.cpit_item).aggregate(max_tax=models.Max('cpit_tax'))['max_tax']
        price_tax = (Decimal(price_tax_per)/Decimal(100) * Decimal(price))
        price_margin = (Decimal(8)/Decimal(100) * Decimal(price))
        item_price, created = priceTable.objects.get_or_create(pt_item=self.cpit_item)
        item_price.pt_sellingPrice = price + price_tax + price_margin
        item_price.save()

    def backup_purchase_item_data(self):
        # Get or create the corresponding purchase backup entry
        cpt_b_backup = self.cpit_billNum.backup_purchase_data()

        # Create the cpit_backup entry
        cpit_backup.objects.create(
            cpit_b_billNum=cpt_b_backup,
            cpit_b_item=self.cpit_item.item_name if self.cpit_item else None,
            cpit_b_qty=self.cpit_qty,
            cpit_b_price=self.cpit_price,
            cpit_b_tax=self.cpit_tax,
            cpit_b_Amount=self.cpit_Amount
        )


class cpt_backup(models.Model):
    cpt_b_billNum = models.CharField(max_length=50, unique=True)
    cpt_b_vendor = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_address = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_gst = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_contact = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_phone = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_date = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_user = models.CharField(max_length=100, null=True, blank=True)
    cpt_b_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cpt_b_billNum


class cpit_backup(models.Model):
    cpit_b_billNum = models.ForeignKey(cpt_backup, on_delete=models.CASCADE)
    cpit_b_item = models.CharField(max_length=100, null=True, blank=True)
    cpit_b_qty = models.PositiveIntegerField(null=True, blank=True)
    cpit_b_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cpit_b_tax = models.PositiveIntegerField(null=True, blank=True)
    cpit_b_Amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.cpit_b_billNum.cpt_b_billNum



# class purchaseorderTable(models.Model):
#     pot_order_number= models.CharField(max_length=20, unique=True)
#     pot_date = models.DateField(auto_now_add=True)
#     pot_vendor = models.ForeignKey(vendorTable, on_delete=models.CASCADE)
#     pot_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     pot_items = models.ManyToManyField(itemTable, through='purchaseorderitemTable')
#
#     def __str__(self):
#         return (self.pot_order_number)
#
# class purchaseorderitemTable(models.Model):
#     oit_purchase_order=models.ForeignKey(purchaseorderTable,on_delete=models.CASCADE)
#     oit_item= models.ForeignKey(itemTable, on_delete=models.CASCADE)
#     oit_quantity = models.PositiveIntegerField(null=True, blank=True)
#     oit_price= models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
#     oit_tax_percentage=models.PositiveIntegerField(null=True, blank=True)
#     oit_totalprice = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.oit_purchase_order.pot_order_number} + {self.oit_item.item_name}"
#
#        def save(self, *args, **kwargs):
#         super(purchaseorderitemTable, self).save(*args, **kwargs)
#         self.update_purchase_stock_qty()
#         self.update_selling_price()
#
#     def update_purchase_stock_qty(self):
#         from Stock.models import stockTable
#         total_quantity = purchaseorderitemTable.objects.filter(oit_item=self.oit_item).aggregate(total=models.Sum('oit_quantity'))['total']
#         stock_item, created = stockTable.objects.get_or_create(st_item=self.oit_item)
#         stock_item.st_purchaseDirectStock = total_quantity
#         stock_item.save()
#
#     def update_selling_price(self):
#         from Core.models import priceTable
#         price = purchaseorderitemTable.objects.filter(oit_item=self.oit_item).aggregate(max_price=models.Max('oit_price'))['max_price']
#         price_tax_per = purchaseorderitemTable.objects.filter(oit_item=self.oit_item).aggregate(max_tax=models.Max('oit_tax_percentage'))['max_tax']
#         price_tax = (Decimal(price_tax_per)/Decimal(100) * Decimal(price))
#         price_margin = (Decimal(8)/Decimal(100) * Decimal(price))
#         item_price, created = priceTable.objects.get_or_create(pt_item=self.oit_item)
#         item_price.pt_sellingPrice = price + price_tax + price_margin
#         item_price.save()
#
#
#  def backup_purchase_data(self):
#         # Create the purchase backup entry only if it doesn't exist
#         cpt_b_backup, created = cpt_backup.objects.get_or_create(
#             cpt_b_billNum=self.cpt_billNum,
#             defaults={
#                 'cpt_b_vendor': self.cpt_vendor.vendor_shop_name,  # Assuming vendorTable has a vendor_shop_name field
#                 'cpt_b_address': self.cpt_vendor.vendor_location,
#                 'cpt_b_gst': self.cpt_vendor.vendor_GST,
#                 'cpt_b_contact': self.cpt_vendor.vendor_name,
#                 'cpt_b_phone': self.cpt_vendor.vendor_phone,
#                 'cpt_b_date': str(self.cpt_date),
#                 'cpt_b_user': self.cpt_user.username  # Assuming User model has a username field
#             }
#         )
#
#         if created:
#             # Backup items related to this purchase only if the backup entry was created
#             for purchase_item in self.confirmpurchaseitemtable_set.all():
#                 cpit_backup.objects.create(
#                     cpit_b_billNum=cpt_b_backup,
#                     cpit_b_item=purchase_item.cpit_item.item_name if purchase_item.cpit_item else None,
#                     cpit_b_qty=purchase_item.cpit_qty,
#                     cpit_b_price=purchase_item.cpit_price,
#                     cpit_b_tax=purchase_item.cpit_tax,
#                     cpit_b_Amount=purchase_item.cpit_Amount
#                 )