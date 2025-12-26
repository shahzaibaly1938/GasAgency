from django.shortcuts import render, redirect
from .models import CustomerPayment
from customer.models import Customer
from sell.models import Sell
from decimal import Decimal
# Create your views here.

def payment_home(request):
    payments = CustomerPayment.objects.all()
    context = { 'payments': payments }
    return render(request, 'payments/home.html', context)

def add_payment(request, sell_id):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        sell_record_id = request.POST.get('sell_record')
        amount_paid = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes', '')


        payment = CustomerPayment(
            customer=Customer.objects.get(id=customer_id),
            sell_record=Sell.objects.get(id=sell_record_id),
            amount_paid=amount_paid,
            payment_date=payment_date,
            payment_method=payment_method,
            notes=notes
        )
        payment.save()
        sell_record = Sell.objects.get(id=sell_record_id)
        
        # Update payment status of the sell record
      
        payment_amount = Decimal(payment.amount_paid)
        total_amount = Decimal(sell_record.total_amount)

        if payment_amount >= total_amount:
            sell_record.payment_status = "paid"
        else:
            sell_record.payment_status = "partialy"
            sell_record.due_amount = total_amount - payment_amount
        
        sell_record.save()
        return redirect('payments_home')


    sell_record = Sell.objects.get(id=sell_id)
    customer = sell_record.customer
    context = {
        'customer': customer,
        'sell_record': sell_record,
    }
    return render(request, 'payments/add_payment.html', context)


def payment_dues(request):
    dues = Sell.objects.filter(payment_status__in=["due", "partialy"])
    context = {
        'dues':dues
    }
    return render(request, 'payments/dues.html', context)

def make_due(request, sell_id):
    sell_record = Sell.objects.get(id=sell_id)
    sell_record.payment_status = "due"
    sell_record.due_amount = sell_record.total_amount
    sell_record.save()
    return redirect('payment_dues')


def payment_process(request, sell_id):
    sell_record = Sell.objects.get(id=sell_id)
    customer = sell_record.customer
    context = {
        'sell_record': sell_record,
        'customer': customer,
    }
    return render(request, 'payments/payment_process.html', context)