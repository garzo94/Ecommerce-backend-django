
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from base.models import Product,CarItems, Review
from rest_framework.views import APIView
from base.serializers import ProductSerializer, CarItemsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import (get_object_or_404)



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
         print(instance,'instanceeasdasd')
         obj = get_object_or_404(CarItems,id_prod=self.kwargs['id_prod'], user= self.request.user)
         obj.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)



class clearCarItems(APIView):
     permission_classes = [IsAuthenticated,]
     def delete(self, request):
        CarItems.objects.filter(user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request,pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    #1 - review alradeady exists
    alreadyExits = product.review_set.filter(user=user).exists()
    if alreadyExits:
        content = {'details':'Prodcut already reviewed'}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    #2 - No ratting or 0
    elif data['rating'] == 0:
        content = {'details':'please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    #3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product = product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total/len(reviews)
        product.save()

        return Response('Review Added')








