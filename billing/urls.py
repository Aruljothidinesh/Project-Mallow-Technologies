from django.urls import path
from .views import billing_page, purchase_list

urlpatterns = [
    path('', billing_page, name='billing_page'),
    path('purchases/', purchase_list, name='purchase_list'),
]