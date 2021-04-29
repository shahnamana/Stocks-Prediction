from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="index"),
    path("stockslist/", views.stockslist, name="stockslist"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("addstocks/<str:name>", views.addstocks, name="addstocks"),
    path("removestocks/<str:name>", views.removestocks, name="removestocks"),
    path("makePredictions/<str:name>", views.makePredictions, name="makePredictions"),
    path("", views.home, name="home")
    
]