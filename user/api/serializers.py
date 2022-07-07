from attr import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import (Category, Order, Product, 
                        Address,Customer, Seller,Payment, 
                        SellerAddress,SellerBankDetail)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
 

    class Meta:
        model = Customer
        fields = ('username', 'password', 'password2', 'email',
                  'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "password fields didn't match"}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            zipcode=validated_data['zipcode'],
            contact=validated_data['contact'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': "password"}, write_only=True)
    city = serializers.CharField(style={'input_type': "text"}, write_only=True)
    state = serializers.CharField(style={'input_type': "text"}, write_only=True)
    pincode = serializers.CharField(
        style={'input_type': "text"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'password2', 'city', 'state', 'pincode']
        extra_kwargs = {
            'first_name': {'required': True, "write_only": True},
            'last_name': {'required': True, "write_only": True},
            'username': {'required': True, "write_only": True},
            'password': {'required': True, "write_only": True},
            'city': {'required': True, "write_only": True},
            'state': {'required': True, "write_only": True},
            'pincode': {'required': True, "write_only": True},
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        city = self.validated_data['city']
        state = self.validated_data['state']
        pincode = self.validated_data['pincode']

        if password != password2:
            raise serializers.ValidationError({
                'error': "password not match"
            })
        user.set_password(password)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user)
        return user


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    

class PaymentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomerListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ["user"]
    
    # get address from address table
    def get_user(self, obj):
        customer_query = User.objects.filter(id=obj.user.id)
        serializer = UserSerializer(customer_query, many=True)
        return serializer.data
    

class UserSerializer(serializers.ModelSerializer):
    delivery_address = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'last_login', 'is_superuser']
    
    # use to get the delivery address
    def get_delivery_address(self, obj):
        customer_address_query = Address.objects.filter(
            customer_id=obj.id)
        serializer = CustomerAddressSerializer(customer_address_query, many=True)
        return serializer.data
    
    # use to get the payment details
    def get_payment(self, obj):
        customer_payment_query = Payment.objects.filter(
            customer_id=obj.id)
        serializer = PaymentAddressSerializer(customer_payment_query, many=True)
        return serializer.data
    
    # use to get the orders details
    def get_orders(self, obj):
        customer_order_query = Order.objects.filter(customer_id=obj.customer.id)
        serializer = OrderSerializer(customer_order_query, many=True)
        return serializer.data


# Seller serializers
class SellerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':"password"},write_only=True)
    mobile_number = serializers.CharField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2','mobile_number']
        extra_kwargs = {
            'password': {'required': True,"write_only":True},
        }
    
    def save(self, **kwargs):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        mobile_number = self.validated_data['mobile_number']
        if password != password2:
            raise serializers.ValidationError({
                'error':"password not match"
            })
        user.set_password(password)
        user.is_seller = True
        user.save()
        Seller.objects.create(user=user,mobile_number=mobile_number)
        return user


class SellerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerAddress
        fields = "__all__"


class SellerProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    bank_details = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'last_login', 
                   'is_superuser']

    # use to get the seller address
    def get_address(self, obj):
        seller = Seller.objects.get(user = obj.id)
        selller_address_query = SellerAddress.objects.filter(seller_id=seller)
        serializer = SellerAddressSerializer(selller_address_query, many=True)
        return serializer.data
    
    # use to get the seller bank details
    def get_bank_details(self, obj):
        seller = Seller.objects.get(user = obj.id)
        selller_bank_query = SellerBankDetail.objects.filter(seller_id=seller)
        serializer = SellerBankDetailsSerializer(selller_bank_query, many=True)
        return serializer.data

class SellerBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerBankDetail
        fields = "__all__"


class SellerDetailSerializer(serializers.ModelSerializer):
    seller_address = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = "__all__"

    # use to get the delivery address
    def get_seller_address(self, obj):
        selller_address_query = SellerAddress.objects.filter(seller_id=obj.id)
        serializer = SellerAddressSerializer(selller_address_query, many=True)
        return serializer.data


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class CategorySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(many=True)

    # To display the subcategory
    def to_representation(self, instance):
        if 'subcategory' not in self.fields:
            self.fields['subcategory'] = CategorySerializer(instance, many=True)
        return super(CategorySerializer, self).to_representation(instance)
   # def get_children(self, instance):
    #     return CategorySerializer(
    #         instance=instance.subcategory.all(), many=True, read_only=True
    #     ).data

    class Meta:
        model = Category
        fields = ['id', 'parent_category', 'name', 'product']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

        extra_kwargs = {
            'price': {'required': True},
            'description': {'required': True},
            'category': {'required': True},
        }

    # To get the forigen key data or products details
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        # remove the products details from nested serializer
        del response["category"]["product"]
        return response


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"