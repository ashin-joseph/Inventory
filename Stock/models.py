from django.db import models
from Purchase.models import itemTable, purchaseorderTable, orderitemTable


class stockTable(models.Model):
    st_item = models.OneToOneField(itemTable, on_delete=models.CASCADE)
    st_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.st_item.item_name}"
