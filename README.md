Django Billing System
A full-featured billing and invoice generation system built using Django.
This project supports product billing, tax calculation, cash denomination handling, invoice generation, and email delivery.
Features
•	Product management (Admin panel)
•	Dynamic billing with multiple products
•	Tax calculation per item
•	Net price and rounded billing
•	Cash paid via denominations
•	Automatic balance calculation
•	Optimal balance denomination breakdown
•	Invoice generation page
•	Email invoice sending via SMTP
•	Purchase history tracking

Project Structure
 
1.Create virtual environment
python -m venv venv
venv\Scripts\activate 

2.Install dependencies
pip install Django

3.Run migrations
python manage.py makemigrations
python manage.py migrate

4.Create superuser
python manage.py createsuperuser
Username : Aruljothi
Password    : 
Confirm Password : 

5.Run server
python manage.py runserver

Billing Logic

1.	Tax Calculation (services.py)

2.	Rounded Net Price (services.py)

3.	Denomination Algorithm

Greedy approach is used:

 System returns optimal balance using available notes.

Denomination Output – page1

4.	Email Configuration (settings.py)

EMAIL_HOST_PASSWORD – Requires Gmail App Password.
 
5.	Billing Page

•	Enter customer email
•	Add multiple products
•	Enter denominations
•	Auto calculate paid amount
 
6. Invoice Page

Displays:
•	Product ID
•	Unit price
•	Purchase price
•	Tax %
•	Tax amount
•	Total per item
•	Total tax payable
•	Rounded net price
•	Balance payable
•	Balance denominations
 


