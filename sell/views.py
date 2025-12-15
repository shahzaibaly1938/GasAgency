from django.shortcuts import render, redirect
from customer.models import Customer
from .models import Sell
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.
def sell_view(request):
    sells = Sell.objects.all().order_by('-date')
    paginator = Paginator(sells, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'sell': page_obj,
    }
    return render(request, 'sell/sell.html', context)

def sell_create_view(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer = request.POST.get('customer')
        no_domestic_cylinder = int(request.POST.get('domestic_number', 0))
        domestic_price = float(request.POST.get('domestic_price', 0.00))
        no_commercial_cylinder = int(request.POST.get('commercial_number', 0))
        commercial_price = float(request.POST.get('commercial_price', 0.00))
        return_domestic_cylinder = int(request.POST.get('domestic_return', 0))
        return_commercial_cylinder = int(request.POST.get('commercial_return', 0))
        total_amount = float(request.POST.get('total_amount', 0.00))
        date = request.POST.get('date', datetime.now())

        customer_instance = Customer.objects.get(id=customer)
        sale = Sell(
            customer=customer_instance,
            no_domestic_cylinder=no_domestic_cylinder,
            domestic_price=domestic_price,
            no_commercial_cylinder=no_commercial_cylinder,
            commercial_price=commercial_price,
            return_domestic_cylinder=return_domestic_cylinder,
            return_commercial_cylinder=return_commercial_cylinder,
            total_amount=total_amount,
            date=date
        )
        sale.save()
        return redirect('payment_process', sell_id=sale.id)                     
        messages.success(request, 'Sale record created successfully.')  
        
    context = {
        'customers': customers,
       
    }
    return render(request, 'sell/sell_create.html', context)

def sell_view_detail(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    context = {
        'sell': sell,
    }
    return render(request, 'sell/sell_view.html', context)

def sell_edit_view(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer = request.POST.get('customer')
        no_domestic_cylinder = int(request.POST.get('domestic_number', 0))
        domestic_price = float(request.POST.get('domestic_price', 0.00))
        no_commercial_cylinder = int(request.POST.get('commercial_number', 0))
        commercial_price = float(request.POST.get('commercial_price', 0.00))
        return_domestic_cylinder = int(request.POST.get('domestic_return', 0))
        return_commercial_cylinder = int(request.POST.get('commercial_return', 0))
        total_amount = float(request.POST.get('total_amount', 0.00))
        date = request.POST.get('date', datetime.now())

        customer_instance = Customer.objects.get(id=customer)
        
        sell.customer = customer_instance
        sell.no_domestic_cylinder = no_domestic_cylinder
        sell.domestic_price = domestic_price
        sell.no_commercial_cylinder = no_commercial_cylinder
        sell.commercial_price = commercial_price
        sell.return_domestic_cylinder = return_domestic_cylinder
        sell.return_commercial_cylinder = return_commercial_cylinder
        sell.total_amount = total_amount
        sell.date = date
        
        sell.save()
        return redirect('sell')
        messages.success(request, 'Sale record updated successfully.')
        
    context = {
        'sell': sell,
        'customers': customers,
    }
    return render(request, 'sell/sell_edit.html', context)


def sell_delete_view(request, sell_id):
    sell = Sell.objects.get(id=sell_id)
    sell.delete()
    messages.success(request, f'Sale record of {sell.customer.name} deleted successfully.')
    return redirect('sell')