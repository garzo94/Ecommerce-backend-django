
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product,CarItems, ShippingAddress, Order, OrderItem
from base.serializers import ProductSerializer, CarItemsSerializer, OrderSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
@api_view(['POST',])
@permission_classes(['IsAuthenticated',])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail':'No order Items'},status=status.HTTP_400_BAD_REQUEST)
    else:

        # creating order
        order = Order.objects.create(
            user=user,
            paymentMethod = 'Paypal',
            taxPrice = 0,
            shippingPrice = 0,
            totalPrice=data['totalPrice']

        )
     # creating shipiing
        shipping = ShippingAddress(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
            )

    # creat order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])
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
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data)