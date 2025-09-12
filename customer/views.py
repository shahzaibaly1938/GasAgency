from django.shortcuts import render

# Create your views here.
def customer_view(request):
    return render(request, 'customer/customer.html', {})