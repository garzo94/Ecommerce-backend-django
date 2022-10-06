from django.urls import path, include
from base.views import users_views as views





urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('profile/', views.getUserProfiel, name='user'),
     path('register/', views.registerUsers, name='user'),
     path('', views.getUsers, name='get-users'),

    ]