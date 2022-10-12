
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product,CarItems, ShippingAddress, Order, OrderItem
from base.serializers import ProductSerializer, CarItemsSerializer, OrderSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail':'No order Items'},status=status.HTTP_400_BAD_REQUEST)
    else:
        # creating order
        #I have to pass an boject of total price of all the shopping
        order = Order.objects.create(
            user=user,
            paymentMethod = 'Paypal',
            taxPrice = 0,
            shippingPrice = 0,
            totalPrice=data['totalPrice']

        )
     # creating shipiing
     # I have to pass and object of address, city, postalcode, country
        ShippingAddress.objects.create(
        order=order,
        address=data['shippingAddress']['address'],
        city=data['shippingAddress']['city'],
        postalCode=data['shippingAddress']['postalcode'],
        shippingPrice=0,
        country=data['shippingAddress']['country'],
        )

    # create order items and set order to orderItem relationship
    # I need to pass an array of objects with id of product, qty, total price of product
        for i in orderItems:
            product = Product.objects.get(_id=i['idprod'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url
            )
    ### update stock
        product.countInStock -= item.qty
        product.save()
    serializer = OrderSerializer(order,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def getOrderById(request,pk):
    user= request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail':'Not autorized to view this order'}, status= status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'detail':'Order not exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@permission_classes([IsAuthenticated,])
def updateOrderToPaid(request,pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = datetime.no2()
    order.svae()
    return Response('Order was paid')