from django.contrib import admin  # can delete as not being used
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products')
]