from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404,redirect
from Core.models import itemTable, companyprofileTable
from Damage.models import damageTable
from Stock.models import stockTable
from django.contrib import messages
from User.decorators import admin_required, staff_required, admin_staff_required
User = get_user_model()

@admin_staff_required
def damage(request):
    base_template = 'user/Index.html' if request.user.role == "Admin" else 'user/staff_index.html'
    company_data = companyprofileTable.objects.get()
    item_data = itemTable.objects.all()
    damage_data = damageTable.objects.all()
    if request.method=="POST":
        itemid=request.POST.get('item_id')
        userid=request.POST.get('userid')
        damage_qty=request.POST.get('damageqty')
        reason=request.POST.get('reason')

        item_instance=get_object_or_404(itemTable,id=itemid)
        stock_instance = get_object_or_404(stockTable, st_item=item_instance)
        user_instance =User.objects.get(id=userid)
        if int(damage_qty) > stock_instance.st_remainingStock:
            messages.error(request, f"Low stock for item: {item_instance.item_name}")
            return redirect(damage)
        obj_damage=damageTable(dpt_item=item_instance,dpt_damage_qty=damage_qty,dpt_reason=reason,dpt_user=user_instance)
        obj_damage.save()
        messages.success(request,f"Updated Damage: {item_instance.item_name}")
    return render(request,"damage/damage_form.html",{'item_data':item_data,'damage_data':damage_data, 'base_template':base_template,'company_data':company_data})
