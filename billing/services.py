from .models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
import math

DENOMINATIONS = [500, 200, 100, 50, 20, 10, 5, 2, 1]

def calculate_bill(cart, paid_amount, available_denoms):
    items = []
    total_without_tax = 0
    total_tax = 0

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(product_id=product_id)
        except ObjectDoesNotExist:    
            continue   

        purchase_price = product.price * qty
        tax = purchase_price * (product.tax_percentage / 100)
        total_price = purchase_price + tax

        items.append({
            "product": product,
            
            "unit_price": product.price,
            "qty": qty,
            "purchase_price": purchase_price,   
            "tax_percent": product.tax_percentage,
            "tax": tax,
            "total": total_price
        })

        total_without_tax += purchase_price
        total_tax += tax

    net_price = total_without_tax + total_tax

    round_down_net_price = int(net_price)   #  round down

    balance = paid_amount - round_down_net_price
    balance_denoms = {}
    remaining = int(balance)

    for denom in DENOMINATIONS:
        count = min(remaining // denom, available_denoms.get(denom, 0))
        if count > 0:
            balance_denoms[denom] = count
            remaining -= denom * count

    return {
        "items": items,
        "total_without_tax": total_without_tax,
        "total_tax": total_tax,
        "net_price": net_price,
        "round_down_net_price": round_down_net_price,
        "balance": balance,
        "balance_denoms": balance_denoms
    }
def send_invoice_email(to_email, bill_data):
    print("📧 EMAIL FUNCTION CALLED")
    print("TO:", to_email)
    subject = "Invoice"
    
    message = "Your invoice details:\n\n"

    for item in bill_data["items"]:
        message += (
            f"{item['product'].name} - "
            f"Qty: {item['qty']} - "
            f"Price: {item['unit_price']} - "
            f"Tax: {item['tax']:.2f} - "
            f"Total: {item['total']:.2f}\n"
        )

    message += f"\nTotal Price without tax: {bill_data['total_without_tax']:.2f}"
    message += f"\nTotal tax payable: {bill_data['total_tax']:.2f}"
    message += f"\nNet price of the purchased item: {bill_data['net_price']:.2f}"
    message += f"\nBalance payable to the customer: {bill_data['balance']:.2f}"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )
    print(" EMAIL SENT FUNCTION COMPLETED")