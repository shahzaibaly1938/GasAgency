from django.shortcuts import render

# Create your views here.
def buy_view(request):
    return render(request, 'buy/buy.html', {})