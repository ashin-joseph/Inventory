from decimal import Decimal, InvalidOperation
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404
from Stock.models import stockTable
from Core.models import itemTable, priceTable
from Damage.models import damageTable
from .models import User
from Purchase.models import confirmPurchaseItemTable
from Sales.models import salesorderItemTable, returnsalesItemTable, salesorderTable, returnSalesTable
from datetime import datetime
from collections import defaultdict
User = get_user_model()



def product_details():
    stockdata =stockTable.objects.all()
    itemdata =itemTable.objects.all()
    stockappendNo=[]
    itemappendName=[]
    itemappendCategory=[]
    for i in itemdata:
        itemappendCategory.append(i.item_category)
        itemappendName.append(i.item_name)
    for i in stockdata:
        if i.st_remainingStock < 10:
            stockappendNo.append(i.st_item.item_name)
    return len(stockappendNo),len(itemappendName), len(set(itemappendCategory))

def todays_offer():
    price_data = priceTable.objects.all()
    offer_list = []
    for i in price_data:
        if i.pt_sellingPrice and i.pt_tax and i.pt_offer:
            try:
                selling_price = Decimal(i.pt_sellingPrice)
                tax = (Decimal(i.pt_tax) / 100) * selling_price
                offer = (Decimal(i.pt_offer) / 100) * selling_price
                offer_amount = selling_price + tax - offer
                i.calculated_price = int(offer_amount)
                # Append the item and its calculated offer amount to the list
                offer_list.append((offer, i))
            except (ValueError, Decimal.InvalidOperation) as e:
                continue
    # Sort the list by offer amount in descending order
    offer_list.sort(reverse=True, key=lambda x: x[0])
    # Extract only the sorted items
    sorted_items = [item for _, item in offer_list]
    return sorted_items

def lowstock_list():
    stockdata= stockTable.objects.all()
    stockappendList=[]
    for i in stockdata:
        if i.st_remainingStock < 10:
            stockappendList.append((i.st_item.item_name,i.st_remainingStock))
    return stockappendList

def user_activity():
    userdata = User.objects.all()
    userlist=[]
    for i in userdata:
        userlist.append((i.username, i.last_login, i.email, i.role, i.is_active))
    return userlist

def purchase_overview():
    products_data = confirmPurchaseItemTable.objects.all()
    purchaseSum = 0
    purchaseNo = set()
    for j in products_data:
        if j.cpit_billNum:
            purchaseNo.add(j.cpit_billNum)
        if j.cpit_Amount:
            purchaseSum += int(j.cpit_Amount)

    return purchaseSum, len(purchaseNo)

def sales_overview():
    sales_data = salesorderItemTable.objects.all()
    salesReturn_data = returnsalesItemTable.objects.all()
    salesSum = 0
    salesNo = set()
    salesReturnSum = 0
    salesReturnNo = set()
    for i in sales_data:
        if i.soit_bill_number:
            salesNo.add(i.soit_bill_number)
        if i.soit_total:
            salesSum += int(i.soit_total)

    for j in salesReturn_data:
        if j.rsit_billNum:
            salesReturnNo.add(j.rsit_billNum)
        if j.rsit_refundAmount:
            salesReturnSum += int(j.rsit_refundAmount)

    return salesSum, len(salesNo), salesReturnSum, len(salesReturnNo)


def daily_salesReport():
    current_date = datetime.now().date()  # Get the current date
    daily_sales = 0
    daily_sales_return = 0
    sales_data = salesorderItemTable.objects.filter(soit_bill_number__sot_date=current_date)
    sales_return_data = returnsalesItemTable.objects.filter(rsit_billNum__rst_date=current_date)
    for j in sales_data:
        daily_sales += j.soit_total
    for j in sales_return_data:
        daily_sales_return += j.rsit_refundAmount
    return ( daily_sales, daily_sales_return )

def daily_damageReport():
    current_date = datetime.now().date()  # Get the current date
    daily_damage = 0

    # Fetch damage data for the current date
    damage_data = damageTable.objects.filter(dpt_timestamp=current_date)

    for item in damage_data:
        # Fetch the price data for the item in the damageTable
        price_data = priceTable.objects.filter(pt_item=item.dpt_item).first()

        if price_data:
            price = price_data.pt_sellingPrice * item.dpt_damage_qty
            tax = int((price_data.pt_tax / 100)) * price
            offer = int((price_data.pt_offer / 100)) * price
            total_d = price + tax - offer
            daily_damage += int(total_d)

    return daily_damage
def daily_purchaseReport():
    current_date = datetime.now().date()  # Get the current date
    daily_purchase = 0
    purchase_data = confirmPurchaseItemTable.objects.filter(cpit_billNum__cpt_date=current_date)
    for i in purchase_data:
        daily_purchase += i.cpit_Amount
    return daily_purchase

def daily_profitReport():
    daily_sales, daily_sales_return = daily_salesReport()
    daily_purchase = daily_purchaseReport()
    daily_damage = daily_damageReport()
    profit = daily_sales - daily_purchase - daily_damage + daily_sales_return
    return int(profit)


def offerAndprice():
    price_data = priceTable.objects.all()
    offer_list = []

    for i in price_data:
        try:
            # Set default values if fields are None
            selling_price = Decimal(i.pt_sellingPrice) if i.pt_sellingPrice else Decimal('0')
            tax = (Decimal(i.pt_tax) / 100) * selling_price if i.pt_tax else Decimal('0')
            offer = (Decimal(i.pt_offer) / 100) * selling_price if i.pt_offer else Decimal('0')

            # Calculate the offer amount
            offer_amount = selling_price + tax - offer
            i.calculated_price = int(offer_amount)

            # Append the item and its calculated offer amount to the list
            offer_list.append((offer_amount, i))
        except (ValueError, InvalidOperation):
            continue

    # Sort the list by calculated offer amount in descending order
    offer_list.sort(reverse=True, key=lambda x: x[0])

    # Extract only the sorted items
    sorted_items = [item for _, item in offer_list]

    return sorted_items



# def todaysoffer():
#     price_data = priceTable.objects.all()
#     total_offer_amount=0
#     for i in price_data:
#         if i.pt_sellingPrice and i.pt_tax and i.pt_offer:
#             selling_price = Decimal(i.pt_sellingPrice)
#             tax=(Decimal(i.pt_tax/100))*selling_price
#             offer=(Decimal(i.pt_offer/100))*selling_price
#             offer_amount = selling_price + tax - offer
#             total_offer_amount += offer_amount
#             i.calculated_price = int(offer_amount)
#     return price_data
