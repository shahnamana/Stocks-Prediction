from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Stock
from statsmodels.tsa.arima_model import ARIMAResults
from django.contrib import messages
from nsetools import Nse
from json import dumps
# from graphos.sources.simple import SimpleDataSource
# from graphos.renderers.yui import LineChart
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
# from graphos.renderers import flot
import pandas as pd
import datetime as dt

# Create your views here.
def index(response):
    return render(response,"main/base.html")

def home(response):
    return render(response,"main/home.html")

def stockslist(response):
    stock_names=[
        "State Bank of India (SBIN)",
        "Housing Development Finance Corporation Limited(HDFC)",
        "Reliance Industries Limited(RELIANCE)",
        "Tata Motors Limited(TATAMOTORS)",
        "Aurobindo Pharma Limited(AUROPHARMA)"
    ]

    # nums=[x+1 for x in range(len(stock_names))]
    symbols=["SBIN","HDFC","RELIANCE","TATAMOTORS","AUROPHARMA"]
    stockPrices_dict={}
    temp={}
    count=0
    for i in symbols:
        stockPrices_dict[i]={}
        temp=getLivePrices(i)
        # print(type(temp))
        # print(temp["lastPrice"])
        stockPrices_dict[i]["symbol"]=stock_names[count]
        stockPrices_dict[i]["lastPrice"]=temp["lastPrice"]
        stockPrices_dict[i]["open"]=temp["open"]
        stockPrices_dict[i]["dayHigh"]=temp["dayHigh"]
        stockPrices_dict[i]["dayLow"]=temp["dayLow"]
        stockPrices_dict[i]["previousClose"]=temp["previousClose"]
        count+=1;
    # print(stockPrices_dict)
    # stockPrices_dict = dict(zip(stock_names, list(stockPrices_dict.values())))
    # stockPrices_dict=getLivePrices(symbols)
    return render(response, "main/stockslist.html",{"prices":stockPrices_dict})

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

def makePredictions(response,name):
    # filename = r"C:\Users\Jay\Desktop\jay_C\jay projects\MIP\Stocks-Prediction\StockPrediction\HDFC_model.pkl"
    filename = "./"+name+"_model.pkl"
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
    # dataJSON = dumps(final_dict)
    print(final_dict)


    data = [['Dates', 'Price']]
    for key, value in final_dict.items():
        data.append([key, value])
    print("\n\n\n\n\n\n\n", data, "\n\n\n\n\n")

    print(type(data[1][0]))
    print(data[1][0])
    # data =  [
    #         ['Year', 'Sales', 'Expenses'],
    #         [2004, 1000, 400],
    #         [2005, 1170, 460],
    #         [2006, 660, 1120],
    #         [2007, 1030, 540]
    #     ]
    # DataSource object
    data_source = SimpleDataSource(data=data)
    # Chart object
    chart = LineChart(data_source)
    print(type(chart))
    # chart = flot.LineChart(data_source)
    context = {'chart': chart}
    return render(response, 'main/graph.html', context)

def getLivePrices(name):
    nse=Nse()
    q=nse.get_quote(name)
    # print(q)
    # stock_names={
    #     "State Bank of India (SBIN)":"SBIN",
    #     "Housing Development Finance Corporation Limited(HDFC)":"HDFC",
    #     "Reliance Industries Limited(RELIANCE)":"RELIANCE",
    #     "Tata Motors Limited(TATAMOTORS)":"TATAMOTORS",
    #     "Aurobindo Pharma Limited(AUROPHARMA)":"AUROPHARMA",
    # }
    # stockPrices_dict={}
    # temp={}
    # for i in symbols:
    #     stockPrices_dict[i]={}
    #     temp=nse.get_quote(i)
    #     # print(type(temp))
    #     # print(temp["lastPrice"])
    #     stockPrices_dict[i]["lastPrice"]=temp["lastPrice"]
    #     stockPrices_dict[i]["open"]=temp["open"]
    #     stockPrices_dict[i]["dayHigh"]=temp["dayHigh"]
    #     stockPrices_dict[i]["dayLow"]=temp["dayLow"]
    #     stockPrices_dict[i]["previousClose"]=temp["previousClose"]
    # new_temp=[]
    # for key,value in stock_names:
    #     if value in symbols:
    #         temp.append(key)
    # # print(stockPrices_dict)
    # stockPrices_dict = dict(zip(new_temp, list(stockPrices_dict.values())))
    return q
