#old sales model
from django.db import models
from Core.models import itemTable, priceTable
from User.models import User


class salesorderTable(models.Model):
    sot_bill_number = models.CharField(max_length=50, unique=True)
    sot_date = models.DateField(auto_now_add=True)
    sot_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sot_items = models.ManyToManyField(itemTable, through='salesorderItemTable')

    def __str__(self):
        return f"{self.sot_bill_number} {self.sot_date}"


    def save(self, *args, **kwargs):
        super(salesorderTable, self).save(*args, **kwargs)
        # Backup data after all items are saved
        self.backup_sales_data()

    def backup_sales_data(self):
        # Create the purchase backup entry only if it doesn't exist
        sot_b_backup, created = sot_backup.objects.get_or_create(
            sot_b_bill_number=self.sot_bill_number,
            defaults={
                'sot_b_date': self.sot_date,
                'sot_b_user': self.sot_user.username
            }
        )
        return sot_b_backup

    # def delete_after_sale_backup(self):
    #     salesorderItemTable.objects.filter(soit_bill_number=self).delete()
    #     self.delete()

class salesorderItemTable(models.Model):
    soit_bill_number = models.ForeignKey(salesorderTable, on_delete=models.CASCADE)
    soit_item = models.ForeignKey(itemTable, on_delete=models.CASCADE)
    soit_quantity = models.PositiveIntegerField(null=True, blank=True)
    soit_price = models.ForeignKey(priceTable, on_delete=models.CASCADE)
    soit_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.soit_bill_number.sot_bill_number

    def save(self, *args, **kwargs):
        super(salesorderItemTable, self).save(*args, **kwargs)
        self.update_sales_stock_qty()
        self.backup_sales_item_data()

    def update_sales_stock_qty(self):
        from Stock.models import stockTable
        total_sales_quantity = \
        salesorderItemTable.objects.filter(soit_item=self.soit_item).aggregate(total=models.Sum('soit_quantity'))[
            'total']
        sales_stock_item, created = stockTable.objects.get_or_create(st_item=self.soit_item)
        sales_stock_item.st_soldStock = total_sales_quantity
        sales_stock_item.save()

    def backup_sales_item_data(self):
        # Get or create the corresponding purchase backup entry
        soit_b_backup = self.soit_bill_number.backup_sales_data()

        # Create the soit_backup entry
        soit_backup.objects.create(
            soit_b_bill_number=soit_b_backup,
            soit_b_item=self.soit_item.item_name if self.soit_item else None,
            soit_b_quantity=self.soit_quantity,
            soit_b_price=self.soit_price.pt_sellingPrice,
            soit_b_tax=self.soit_price.pt_tax,
            soit_b_offer=self.soit_price.pt_offer,
            soit_b_total=self.soit_total
        )



class returnSalesTable(models.Model):
    rst_billNum = models.CharField(max_length=50, unique=True)
    rst_poNum = models.CharField(max_length=50)
    rst_date = models.DateField(auto_now_add=True)
    rst_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rst_item = models.ManyToManyField(itemTable, through='returnsalesItemTable')

    def __str__(self):
        return self.rst_billNum

    def save(self, *args, **kwargs):
        super(returnSalesTable, self).save(*args, **kwargs)
        self.backup_returnsale_data()

    def backup_returnsale_data(self):
        rst_b_backup, created = rst_backup.objects.get_or_create(
            rst_b_billNum=self.rst_billNum,
            defaults={
                'rst_b_poNum': self.rst_poNum,
                'rst_b_date': self.rst_date,
                'rst_b_user': self.rst_user.username
            }
        )
        return rst_b_backup

    # def delete_after_return_backup(self):
    #     returnsalesItemTable.objects.filter(rsit_billNum=self).delete()
    #     self.delete()

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
        self.backup_returnsale_item_data()

    def update_return_sales_stock_qty(self):
        from Stock.models import stockTable
        total_quantity = \
        returnsalesItemTable.objects.filter(rsit_item=self.rsit_item).aggregate(total=models.Sum('rsit_qty'))['total']
        stock_item, created = stockTable.objects.get_or_create(st_item=self.rsit_item)
        stock_item.st_salesReturnStock = total_quantity
        stock_item.save()

    def backup_returnsale_item_data(self):
        rsit_b_backup = self.rsit_billNum.backup_returnsale_data()

        # Create the rsit_backup entry
        rsit_backup.objects.create(
            rsit_b_billNum=rsit_b_backup,
            rsit_b_item=self.rsit_item.item_name if self.rsit_item else None,
            rsit_b_reason=self.rsit_reason,
            rsit_b_qty=self.rsit_qty,
            rsit_b_price=self.rsit_price,
            rsit_b_tax=self.rsit_tax,
            rsit_b_offer=self.rsit_offer,
            rsit_b_refundAmount=self.rsit_refundAmount
        )


class sot_backup(models.Model):
    sot_b_bill_number = models.CharField(max_length=50, unique=True)
    sot_b_date = models.CharField(max_length=100, null=True, blank=True)
    sot_b_user = models.CharField(max_length=100, null=True, blank=True)
    sot_b_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sot_b_bill_number} {self.sot_b_date}"

class soit_backup(models.Model):
    soit_b_bill_number = models.ForeignKey(sot_backup, on_delete=models.CASCADE)
    soit_b_item = models.CharField(max_length=100, null=True, blank=True)
    soit_b_quantity = models.PositiveIntegerField(null=True, blank=True)
    soit_b_price = models.CharField(max_length=100, null=True, blank=True)
    soit_b_tax = models.CharField(max_length=100, null=True, blank=True)
    soit_b_offer = models.CharField(max_length=100, null=True, blank=True)
    soit_b_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.soit_b_bill_number.sot_b_bill_number

class rst_backup(models.Model):
    rst_b_billNum = models.CharField(max_length=50, unique=True)
    rst_b_poNum = models.CharField(max_length=100, null=True, blank=True)
    rst_b_date = models.CharField(max_length=100, null=True, blank=True)
    rst_b_user = models.CharField(max_length=100, null=True, blank=True)
    sot_b_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rst_b_billNum} {self.rst_b_date}"

class rsit_backup(models.Model):
    rsit_b_billNum = models.ForeignKey(rst_backup, on_delete=models.CASCADE)
    rsit_b_item = models.CharField(max_length=100, null=True, blank=True)
    rsit_b_reason = models.CharField(max_length=100, null=True, blank=True)
    rsit_b_qty = models.PositiveIntegerField(null=True, blank=True)
    rsit_b_price = models.CharField(max_length=100, null=True, blank=True)
    rsit_b_tax = models.CharField(max_length=100, null=True, blank=True)
    rsit_b_offer = models.CharField(max_length=100, null=True, blank=True)
    rsit_b_refundAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.rsit_b_billNum.rst_b_billNum
