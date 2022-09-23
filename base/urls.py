from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()

router.register('car', views.getItemsCar, basename='caritems')
urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
    path('', views.getRoutes, name='routes'),
     path('users/profile/', views.getUserProfiel, name='user'),
    path('products/', views.getProducts, name='products'),
    path('products/<str:pk>/', views.getProduct, name='product'),
    ]