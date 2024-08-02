from django.shortcuts import render,get_object_or_404,redirect
from Core.models import itemTable
from Damage.models import damageTable
from Stock.models import stockTable
from django.contrib import messages
from User.decorators import admin_required, staff_required, admin_staff_required
@admin_staff_required
def damage(request):
    item_data = itemTable.objects.all()
    damage_data = damageTable.objects.all()
    if request.method=="POST":
        itemid=request.POST.get('item_id')
        damage_qty=request.POST.get('damageqty')

        item_instance=get_object_or_404(itemTable,id=itemid)
        stock_instance = get_object_or_404(stockTable, st_item=item_instance)
        if int(damage_qty) > stock_instance.st_remainingStock:
            messages.error(request, f"Low stock for item: {item_instance.item_name}")
            return redirect(damage)
        obj_damage=damageTable(dpt_item=item_instance,dpt_damage_qty=damage_qty)
        obj_damage.save()
        messages.info(request,f"Updated Damage: {item_instance.item_name}")
    return render(request,"damage/damage_form.html",{'item_data':item_data,'damage_data':damage_data})
