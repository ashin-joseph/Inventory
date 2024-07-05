from django.shortcuts import render,get_object_or_404
from Core.models import itemTable
from Damage.models import damageTable

def damage(request):
    item_data = itemTable.objects.all()
    damage_data = damageTable.objects.all()
    if request.method=="POST":
        itemid=request.POST.get('item_id')
        damage_qty=request.POST.get('damageqty')
        item_instance=get_object_or_404(itemTable,id=itemid)
        obj_damage=damageTable(dpt_item=item_instance,dpt_damage_qty=damage_qty)
        obj_damage.save()
    return render(request,"damage/damage_form.html",{'item_data':item_data,'damage_data':damage_data})
