from django.urls import path
from . import views
urlpatterns = [
    path("index/", views.index, name="index"),
    path("stockslist/", views.stockslist, name="stockslist"),
    path("", views.home, name="home")
    
]