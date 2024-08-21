from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from Stock.models import stockTable


@receiver(user_logged_in)
def send_login_alert(sender, request, user, **kwargs):
    subject = "User Logged In"
    message = f"User {user.username} with role {user.role} has logged in to StockSmart."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.ADMIN_EMAIL]

    send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=stockTable)
def check_stock_alert(sender, instance, **kwargs):
    if instance.st_remainingStock < 5:
        subject = "Low Stock Alert"
        message = f"The stock for {instance.st_item.item_name} is below the required level. Current quantity: {instance.st_remainingStock}."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]

        send_mail( subject, message, from_email, recipient_list, fail_silently=False)
