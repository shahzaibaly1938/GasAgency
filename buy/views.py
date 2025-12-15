from django.shortcuts import render
from vendor.models import Vendor
from .models import AddStock
from datetime import datetime
from django.contrib import messages

# Create your views here.
def buy_view(request):
    stock = AddStock.objects.all().order_by('-date')
    context = { 
        'stock' : stock }
    return render(request, 'buy/buy.html', context)



def add_stock_view(request):
    vendors = Vendor.objects.all()
    if request.method == 'POST':
        vendor = request.POST.get('customer')
        no_domestic_cylinder = int(request.POST.get('domestic_number', 0))
        domestic_price = float(request.POST.get('domestic_price', 0.00))
        no_commercial_cylinder = int(request.POST.get('commercial_number', 0))
        commercial_price = float(request.POST.get('commercial_price', 0.00))
        return_domestic_cylinder = int(request.POST.get('domestic_return', 0))
        return_commercial_cylinder = int(request.POST.get('commercial_return', 0))
        total_amount = float(request.POST.get('total_amount', 0.00))
        date = request.POST.get('date', datetime.now())

        vendor_instance = Vendor.objects.get(id=vendor)
        stock = AddStock( 
            vendor=vendor_instance,
            no_domestic_cylinder=no_domestic_cylinder,
            domestic_price=domestic_price,
            no_commercial_cylinder=no_commercial_cylinder,
            commercial_price=commercial_price,
            return_domestic_cylinder=return_domestic_cylinder,
            return_commercial_cylinder=return_commercial_cylinder,
            total_amount=total_amount,
            date=date
         )
        stock.save()
        messages.success(request, 'Sale record created successfully.')

    context = {
        'vendors': vendors
    }
    return render(request, 'buy/add_stock.html', context)