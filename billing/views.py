from django.shortcuts import render, redirect
from .forms import BillingForm
from .models import Purchase, PurchaseItem, Product
from .services import calculate_bill
from .services import send_invoice_email

def billing_page(request):
    denominations = [500, 200, 100, 50, 20, 10, 5, 2, 1]   

    if request.method == "POST":
        if request.POST.get("action") == "cancel":
            return redirect("billing_page") 
        form = BillingForm(request.POST)

        cart = {}
        for key, value in request.POST.items():
            if key.startswith("product_"):
                index = key.split("_")[1]
                product_id = value
                qty = int(request.POST.get(f"quantity_{index}", 0))
                if product_id and qty:
                    cart[product_id] = qty

        available_denoms = {}
        for denom in denominations:
            available_denoms[denom] = int(request.POST.get(f"denom_{denom}", 0))

        if form.is_valid():
            invalid_products = []

            for pid in cart.keys():
                if not Product.objects.filter(product_id=pid).exists():
                    invalid_products.append(pid)

            if invalid_products:
                return render(request,"billing/page1.html",{
                    "form": form,
                    "denominations": denominations,
                    "error": f"Invalid product IDs: {', '.join(invalid_products)}"
                })        
            result = calculate_bill(cart, form.cleaned_data["paid_amount"], available_denoms)

            purchase = Purchase.objects.create(
                customer_email=form.cleaned_data["customer_email"],
                total_without_tax=result["total_without_tax"],
                total_tax=result["total_tax"],
                net_price=result["net_price"],
                paid_amount=form.cleaned_data["paid_amount"],
                balance=result["balance"],
            )

            for item in result["items"]:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=item["product"],
                    quantity=item["qty"],
                    unit_price=item["unit_price"],
                    tax_amount=item["tax"],
                    total_price=item["total"],
                )

            customer_email = form.cleaned_data["customer_email"]
            send_invoice_email(
                 customer_email,
                result
            )
            return render(request, "billing/page2.html", {
                "data": result,
                "purchase": purchase
            })

    else:
        form = BillingForm()

    return render(request, "billing/page1.html", {
        "form": form,
        "denominations": denominations   #  send to template
    })

def purchase_list(request):
    purchases = Purchase.objects.all().order_by("-created_at")
    return render(request, "billing/purchase_list.html", {"purchases": purchases})
"""
def billing_view(request):
    cart = request.session.get("cart", {})
    paid_amount = float(request.POST.get("paid_amount"))
    available_denoms = request.session.get("denoms", {})

    bill_data = calculate_bill(cart, paid_amount, available_denoms)

    #  SEND EMAIL
    send_invoice_email(
        "aru@gmail.com",
        bill_data
    )

    return render(request, "billing/invoice.html", {"bill": bill_data})
"""    