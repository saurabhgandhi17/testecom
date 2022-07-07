from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView)
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework.views import APIView

from .serializers import (UserSerializer, RegisterSerializer,
                          CustomTokenObtainSerializer, CategorySerializer,
                          ProductSerializer, OrderSerializer,
                          CustomerAddressSerializer, CustomerRegisterSerializer,
                          SellerRegistrationSerializer, PaymentAddressSerializer,
                          SellerDetailSerializer, SellerAddressSerializer, SellerProfileSerializer,
                          SellerBankDetailsSerializer)
from user.models import (Category, Payment, Product,
                         Order, Address, Customer, Seller, SellerBankDetail)


User = get_user_model()


'''
view use to store customers
'''
class CustomerCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    queryset = Customer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'Message': 'Records successfully created',
            'status': status.HTTP_201_CREATED,
            'data': UserSerializer(user, context=self.get_serializer_context()).data},
            status=status.HTTP_201_CREATED)


'''
view use to store customers address details
'''
class CustomerAddressListCreateViewSet(generics.ListCreateAPIView):
    serializer_class = CustomerAddressSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Address.objects.all()

    def put(self, request, pk, format=None):
        address = self.get_object(pk)
        serializer = CustomerAddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Message': 'Address successfully added',
                'status': status.HTTP_201_CREATED,
                'data': serializer.data},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CustomerAddressSerializer(queryset, many=True)
        return Response({
            'Message': 'Address successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data},
            status=status.HTTP_200_OK)


'''
view use to store customers payments details
'''
class CustomerPaymentListCreateViewSet(generics.ListCreateAPIView):
    serializer_class = PaymentAddressSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Payment.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PaymentAddressSerializer(queryset, many=True)
        return Response({
            'Message': 'Payment successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data},
            status=status.HTTP_200_OK)


'''
view use to list all the customers
'''
class CustomerListAPIView(generics.ListAPIView):
    # exclude admin record
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'Message': 'Records successfully fetched',
            'status': status.HTTP_200_OK,
            'total_records': queryset.count(),
            'data': serializer.data}, status=status.HTTP_200_OK)


'''
view use to fetch all details of currently login user
'''
class MyDetailAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'Message': 'Record successfully fetched',
            'status': status.HTTP_200_OK, "data": serializer.data},
            status=status.HTTP_200_OK)


'''
view use to fetch all orders of currently login user
'''
class MyOrdersAPIView(APIView):
    def get(self, request):
        orders = Order.objects.filter(customer=request.user.customer)
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'Message': 'Order(s) successfully fetched',
            'status': status.HTTP_200_OK, "data": serializer.data},
            status=status.HTTP_200_OK)


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainSerializer


# seller with APIViews
class SellerRegisterAPIView(APIView):
    serializer_class = SellerRegistrationSerializer

    def post(self, request, format=None):
        '''
        Register the seller with given seller data
        '''
        serializer = SellerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Message': 'Registration Successfully',
                'status': "success",
                'data': serializer.data},
                status=status.HTTP_201_CREATED)
        else:
            return Response({
                'Message': 'Registration Failed',
                'status': "error",
                'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


class SellerDetailAPIView(APIView):
    """
    Retrieve, update or delete a seller instance.
    """
    def get(self, request, pk, format=None):
        '''
        Retrieves the seller with given seller_id
        '''
        try:
            seller = Seller.objects.get(pk=pk)
            serializer = SellerDetailSerializer(seller)
            return Response({
                'Message': 'Seller Successfully fetched',
                'status': "success",
                'data': serializer.data},
                status=status.HTTP_200_OK)
        except:
            return Response({
                'Message': 'Seller does not exists',
                'status': "success",
                'data': []},
                status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        '''
        Updates the seller with given seller_id if exists
        '''
        seller = Seller.objects.get(pk=pk)
        serializer = SellerDetailSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Message': 'Seller Successfully updated',
                'status': "success",
                'data': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response({
                'Message': 'Seller not updated',
                'status': "error",
                'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        '''
        Deletes the seller with given seller_id if exists
        '''
        try:
            seller = Seller.objects.get(pk=pk)
            seller.delete()
            return Response({
                'Message': 'Seller deleted',
                'status': "success",
                'data': []},
                status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'Message': 'Seller does not exists',
                'status': "success",
                'data': []},
                status=status.HTTP_404_NOT_FOUND)


class SellerAddressAPIView(APIView):
    def post(self, request, format=None):
        '''
        Add the sellers address
        '''
        serializer = SellerAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Message': 'Address Successfully added',
                'status': "success",
                'data': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response({
                'Message': 'Updatation Failed',
                'status': "error",
                'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


class SellerProfileAPIView(APIView):
    def get(self, request):
        serializer = SellerProfileSerializer(request.user)
        return Response({
            'Message': 'Record successfully fetched',
            'status': status.HTTP_200_OK, "data": serializer.data},
            status=status.HTTP_200_OK)
    

class SellerBankDetailsAPIView(APIView):
    def post(self, request, format=None):
        '''
        Add the sellers bank-details
        '''
        serializer = SellerBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Message': 'Bank-details Successfully added',
                'status': "success",
                'data': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response({
                'Message': 'Updatation Failed',
                'status': "error",
                'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'Message': 'You have successfully register',
            'data': serializer.data,
            'status': status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
            headers=headers)


class UsersListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response({
            'Message': 'Records successfully fetched',
            'status': status.HTTP_200_OK,
            'total_records': queryset.count(),
            'data': serializer.data}, status=status.HTTP_200_OK)


class CategoryViewSet(GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'Message': 'Records successfully created',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'Message': 'Records successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response({
            'Message': 'Record successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'Message': 'Records successfully created',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'Message': 'Records successfully fetched',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response({
            'Message': 'Record successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        product = self.get_object()
        product.delete()
        return Response({
            'Message': 'Record successfully deleted',
            'status': status.HTTP_204_NO_CONTENT, },
            status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'Message': 'Your order(s) successfully placed',
            'status': status.HTTP_201_CREATED,
            'data': serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'Message': 'Order(s) successfully fetched',
            'status': status.HTTP_200_OK,
            'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        check_order = Order.objects.filter(id=pk)
        if check_order:
            order = self.get_object()
            order.delete()
            return Response({
                'Message': 'Your order successfully deleted',
                'status': status.HTTP_204_NO_CONTENT, },
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'Message': 'Order not found',
                'status': status.HTTP_200_OK, },
                status=status.HTTP_200_OK)


# Get all orders of current users
class CartViewSet(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            order = get_object_or_404(self.queryset, customer=user)
            serializer = OrderSerializer(order)
            return Response({
                'Message': 'Your order(s)',
                'status': status.HTTP_200_OK, 'data': [serializer.data]},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'Message': 'Your cart is empty',
                'status': status.HTTP_200_OK, "data": []},
                status=status.HTTP_200_OK)
