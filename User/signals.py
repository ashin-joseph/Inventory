from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.conf import settings
from Stock.models import stockTable
from Core.models import companyprofileTable


pdf_requested = Signal()


@receiver(user_logged_in)
def send_login_alert(sender, request, user, **kwargs):
    company_profile = companyprofileTable.objects.first()  # Adjust this if you have multiple company profiles
    company_email = company_profile.company_email if company_profile else None

    if company_email:
        send_mail(
            f"User Logged In: {user.username} ",
            f"Dear {company_profile.company_person},\n\n"
            f"Welcome to StockSmart! \n"
            f"User {user.username}({user.role}) has logged into {company_profile.company_name}'s StockSmart account.\n\n"
            f"Best regards,\n" 
            f"{company_profile.company_name}.",
            "at.stocksmart@gmail.com",  # Default sender
            [company_email],
            fail_silently=False,
        )

    # subject = "User Logged In"
    # message = f"User {user.username} with role {user.role} has logged in to StockSmart."
    # from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = [settings.ADMIN_EMAIL]
    #
    # send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=stockTable)
def check_stock_alert(sender, instance, **kwargs):
    company_profile = companyprofileTable.objects.first()  # Adjust this if you have multiple company profiles
    company_email = company_profile.company_email if company_profile else None

    if company_email and instance.st_remainingStock < int(company_profile.company_threshold_Stock):
        # Send email alert
        send_mail(
            "Low Stock Alert",
            f"Dear {company_profile.company_person},\n\n"
            f"Welcome to StockSmart! \n"
            f"Alert from '{company_profile.company_name}' Inventory: The stock for {instance.st_item.item_name} has fallen below the threshold level. \n {instance.st_item.item_name} : {instance.st_remainingStock}.\n\n"
            f"Best regards,  \n" 
            f"{company_profile.company_name}.",
            "at.stocksmart@gmail.com",  # Default sender email
            [company_email],  # Recipient email in a list
            fail_silently=False,
        )

    # if instance.st_remainingStock < 5:
    #     subject = "Low Stock Alert"
    #     message = f"The stock for {instance.st_item.item_name} is below the required level. Current quantity: {instance.st_remainingStock}."
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [settings.ADMIN_EMAIL]
    #
    #     send_mail( subject, message, from_email, recipient_list, fail_silently=False)
