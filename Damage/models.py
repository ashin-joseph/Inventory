from django.db import models
from Core.models import itemTable
from User.models import User


class damageTable(models.Model):
    dpt_item = models.ForeignKey(itemTable, on_delete=models.CASCADE)
    dpt_damage_qty = models.PositiveIntegerField(null=True, blank=True)
    dpt_reason = models.CharField(max_length=200, null=True, blank=True)
    dpt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    dpt_timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.dpt_item.item_name}"

    def save(self, *args, **kwargs):
        super(damageTable, self).save(*args, **kwargs)
        self.update_damage_stock_qty()

    def update_damage_stock_qty(self):
        from Stock.models import stockTable
        total_damage_quantity = damageTable.objects.filter(dpt_item=self.dpt_item).aggregate(total=models.Sum('dpt_damage_qty'))['total']
        stock_damage, created = stockTable.objects.get_or_create(st_item=self.dpt_item)
        stock_damage.st_damageStock = total_damage_quantity or 0
        stock_damage.save()
