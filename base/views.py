from tkinter.messagebox import NO
from urllib import request
from django.shortcuts import render
from django.http import JsonResponse


from .products import products
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product,CarItems
from base.serializers import ProductSerializer, CarItemsSerializer, UserSerializer, UserSerializerWithToken
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # data['username'] = self.user.username
        # data['email'] = self.user.email
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = ['/api/products/',
    '/api/products/created',
    '/api/products/upload',
    '/api/products/<id>/reviews/',
    '/api/products/top/',
    '/api/products/<id>/',
    '/api/products/delete/<id>/',
    '/api/products/<update>/<id>/']
    return  Response(routes)


@api_view(['GET'])
def getUserProfiel(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)

class getItemsCar(ModelViewSet):
    serializer_class = CarItemsSerializer
    lookup_field = 'id_prod'
    def get_queryset(self):
       return CarItems.objects.filter(user=self.request.user.id)




