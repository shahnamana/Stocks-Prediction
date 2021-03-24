from django.shortcuts import render
from django.http import HttpResponse
from main.models import Investor, Stock
# Create your views here.
def index(response):
    i=Investor.objects.get(name="Jay Shah")
    t=Stock.objects.filter(investor=i)
    print(t)
    return render(response,"main/base.html")

def home(response):
    return render(response,"main/home.html")

def stockslist(response):
    return render(response, "main/stockslist.html")