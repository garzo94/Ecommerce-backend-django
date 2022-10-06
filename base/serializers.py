
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Product, CarItems
from rest_framework_simplejwt.tokens import RefreshToken

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CarItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarItems
        fields = ['id_prod', 'total']

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','_id', 'username','name','isAdmin']

    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

    def get_name(self,obj): #adding a name field using firstname by default
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','_id', 'username','name','email','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)