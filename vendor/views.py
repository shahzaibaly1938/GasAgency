from django.shortcuts import render, redirect
from .models import Vendor
from django.contrib import messages
# Create your views here.

def vednor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors,
    }                   
    return render(request, 'vendor/vendor_list.html', context)   


def create_vendor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        vendor = Vendor(name=name, phone_number=phone, address=address)
        vendor.save()
        messages.success(request, f'vendor: {vendor.name} created successfully.')
        return redirect('vendor_list')
        
        
    return render(request, 'vendor/create_vendor.html', {})

def update_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    if request.method == 'POST':
        vendor.name = request.POST.get('name')
        vendor.phone_number = request.POST.get('phone')
        vendor.address = request.POST.get('address')
        vendor.save()
        messages.success(request, f'Customer: {vendor.name} updated successfully.')
        return redirect('vendor_list')
    context = {
        'vendor': vendor
    }
    return render(request, 'vendor/vendor_update.html', context)

def vendor_details(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'vendor': vendor
    }
    return render(request, 'vendor/vendor_details.html', context)

def delete_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.delete()
    messages.success(request, f'vendor: {vendor.name} Deleted successfully.')
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'vendor/vendor_list.html', context)