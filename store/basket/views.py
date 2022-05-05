from django.shortcuts import render

# Create your views here.
app_name = 'basket'

def basket_summary(request):
    return render(request, 'poll/basket/summary.html')