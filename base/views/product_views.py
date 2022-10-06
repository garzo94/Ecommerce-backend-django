
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product,CarItems
from base.serializers import ProductSerializer, CarItemsSerializer
from rest_framework.viewsets import ModelViewSet


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