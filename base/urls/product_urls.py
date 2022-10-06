from django.urls import path, include
from base.views import product_views as views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()

router.register('car', views.getItemsCar, basename='caritems')
urlpatterns = [
    path('', include(router.urls)),
    path('all/', views.getProducts, name='products'),
    path('<str:pk>/', views.getProduct, name='product'),
    ]