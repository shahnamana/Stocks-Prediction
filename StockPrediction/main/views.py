from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Stock
from statsmodels.tsa.arima_model import ARIMAResults
from django.contrib import messages
import pandas as pd
import datetime as dt

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

def workdays(d, end, excluded=(6, 7)):
    days = []
    while d.date() <= end.date():
        if d.isoweekday() not in excluded:
            days.append(d)
        d += dt.timedelta(days=1)
    return days

def makePredictions(response):
    # filename = r"C:\Users\Jay\Desktop\jay_C\jay projects\MIP\Stocks-Prediction\StockPrediction\HDFC_model.pkl"
    filename = "./HDFC_model.pkl"
    loaded = ARIMAResults.load(filename)
    # index_future_dates = pd.date_range(start=dt.datetime.now(), end=dt.datetime.now()+dt.timedelta(days=20))
    # pred = loaded.predict(start=2038, end=2038+len(index_future_dates)-1, typ="levels").rename("ARIMA PREDICTIONS")
    # print(pred)
    index_future_dates = workdays(dt.datetime(2021, 3, 25), dt.datetime.now() + dt.timedelta(days=20))
    pred = loaded.predict(start=2038, end=2037+len(index_future_dates), typ='levels').rename('ARIMA PREDICTIONS')
    # print(pred)
    pred.index = index_future_dates
    pred = pred[dt.datetime.now():]
    dates = list(pred[dt.datetime.now():].index)
    # index_future_dates = list(pred.index)
    pred=pred.iloc[:10]
    pred = pred.tolist()
    pred = [round(myFloat, 2) for myFloat in pred]
    date_time = [curDT.strftime("%d/%m/%Y") for curDT in dates]
    # index_future_dates = list(pred.index)
    final_dict = dict(zip(date_time[:10], pred))
    return render(response, 'main/home.html', {'values':pred, 'final_dict':final_dict })
    # pred = pred[dt.datetime.now():]
    # index_future_dates = list(pred.index)
    # pred=pred.iloc[-10:]
    # pred = pred.tolist()
    
    # final_dict = dict(zip(index_future_dates[-10:], pred))
    # return render(response, 'main/home.html', {'values':pred, 'final_dict':final_dict })
        