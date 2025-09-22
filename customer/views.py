from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages

# Create your views here.
def customer_view(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customer/customer.html', context)

def create_customer_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        type = request.POST.get('type')
        address = request.POST.get('address')
        customer = Customer(name=name, phone=phone, type=type, address=address)
        customer.save()
        messages.success(request, f'Customer: {customer.name} created successfully.')
        return redirect('customer')
        
        
    return render(request, 'customer/create_customer.html', {})

def update_customer_view(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.type = request.POST.get('type')
        customer.address = request.POST.get('address')
        customer.save()
        messages.success(request, f'Customer: {customer.name} updated successfully.')
        return redirect('customer')
    context = {
        'customer': customer
    }
    return render(request, 'customer/edit_customer.html', context)

def customer_detail_view(request, id):
    customer = Customer.objects.get(id=id)
    context = {
        'customer': customer
    }
    return render(request, 'customer/customer_details.html', context)

def delete_customer_view(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    messages.success(request, f'Customer: {customer.name} Deleted successfully.')
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customer/customer.html', context)