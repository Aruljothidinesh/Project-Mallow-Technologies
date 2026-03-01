from django import forms

class BillingForm(forms.Form):
    customer_email = forms.EmailField(label="Customer Email")
    paid_amount = forms.FloatField(
        label="Cash paid by customer",   #  label shown in UI
        required=False
    )    