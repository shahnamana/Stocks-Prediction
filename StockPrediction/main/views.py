from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Stock
from django.contrib import messages
# Create your views here.
def index(response):
    return render(response,"main/base.html")

def home(response):
    return render(response,"main/home.html")

def stockslist(response):
    stocklist=["SBI","HDFC","RELIANCE","TATA MOTORS","AUROPHARMA"]

    return render(response, "main/stockslist.html",{"sl":stocklist})

def portfolio(response):
    sl=Stock.objects.filter(investor=response.user)
    return render(response, "main/portfolio.html",{"sl":sl})

def addstocks(response,name):
    stocks=Stock.objects.filter(investor=response.user)
    stocks=list(stocks)
    temp=[]
    for i in stocks:
        temp.append(i.stock_name)

    flag = 0
    for i in temp:
        if name==i:
            flag = 1
    if flag == 1:
        messages.error(response,"Stock already added in portfolio")
        return HttpResponseRedirect("/stockslist/")
    elif flag == 0:
        stock=Stock.objects.create(investor=response.user,stock_name=name)
        stock.save()
        messages.success(response,"Stock added in portfolio successfully")
    return HttpResponseRedirect("/stockslist/")

def removestocks(response,name):
    stock=Stock.objects.get(investor=response.user,stock_name=name)
    stock.delete()
    messages.success(response,"Stock deleted from portfolio successfully")
    return HttpResponseRedirect("/portfolio")
        