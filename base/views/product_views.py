
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product,CarItems
from base.serializers import ProductSerializer, CarItemsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)



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
    permission_classes = [IsAuthenticated,]
    serializer_class = CarItemsSerializer
    lookup_field = 'id_prod'
    def get_queryset(self):
       return CarItems.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer, *args, **kwargs):
            serializer.save(user=self.request.user,id_prod=self.request.data['id_prod'], total=self.request.data['total'])

    def perform_update(self, serializer):

         id = self.kwargs['id_prod']
         total = self.request.data['total']
         serializer.save(user=self.request.user, total=total)
    def perform_destroy(self, instance):

         obj = get_object_or_404(CarItems,id_prod=self.kwargs['id_prod'], user= self.request.user)
         obj.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)



