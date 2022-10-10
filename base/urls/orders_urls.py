from django.urls import path, include
from base.views import orders_views as views



urlpatterns = [
    path('add/', views.addOrderItems, )
    ]