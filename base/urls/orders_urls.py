from django.urls import path, include
from base.views import orders_views as views



urlpatterns = [
    path('add/', views.addOrderItems, ),
    path('<str:pk>/', views.getOrderById, name='user-order', ),
    path('<str:pk>/pay', views.updateOrderToPaid, name='pay', ),
    ]