from celery import shared_task
from django.core.mail import send_mail
from .models import Purchase

@shared_task
def send_invoice_email(purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)

    message = f"""
    Invoice

    Total: {purchase.net_price}
    Paid: {purchase.paid_amount}
    Balance: {purchase.balance}
    """

    send_mail(
        subject="Your Invoice",
        message=message,
        from_email="aruljothidinesh25@gmail.com",
        recipient_list=[purchase.customer_email],
    )