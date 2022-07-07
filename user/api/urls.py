from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ProductViewSet, CustomObtainTokenPairView, CategoryViewSet,
                    OrderViewSet, CartViewSet, CustomerAddressListCreateViewSet,
                    CustomerCreateAPIView, SellerBankDetailsAPIView, SellerRegisterAPIView, SellerDetailAPIView,
                    CustomerPaymentListCreateViewSet, CustomerListAPIView,
                    MyDetailAPIView, MyOrdersAPIView, SellerAddressAPIView,SellerProfileAPIView)

app_name = "user_api"

router = SimpleRouter()
router.register('category', CategoryViewSet)
router.register('product', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Endpoints related to customer
    path('customers/register/', CustomerCreateAPIView.as_view(), name='customer'),
    path('customers/address/', CustomerAddressListCreateViewSet.as_view(), name='address'),
    path('customers/payment/', CustomerPaymentListCreateViewSet.as_view(), name='payment'),
    path('customers/info/', MyDetailAPIView.as_view(), name='my_info'),
    path('customers/myorders/', MyOrdersAPIView.as_view(), name='my_info'),


    # Endpoints related to seller
    path('sellers/register/', SellerRegisterAPIView.as_view(), name='seller'),
    path('sellers/<int:pk>/', SellerDetailAPIView.as_view(), name='seller_details'),
    path('sellers/profile/', SellerProfileAPIView.as_view(), name='seller_profile'),
    path('sellers/address/', SellerAddressAPIView.as_view(), name='seller_address'),
    path('sellers/bankdetails/', SellerBankDetailsAPIView.as_view(), name='seller_bankdetails'),


    path('customers/', CustomerListAPIView.as_view(), name='customer_all'), # need to change. only admin can see all the records
    # path('sellers/', CustomerListAPIView.as_view(), name='sellers_all'), # need to change. only admin can see all the records
    
    # path('users/', UsersListView.as_view(), name='users'),
    path('users/login/', CustomObtainTokenPairView.as_view(),name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/cart/', CartViewSet.as_view(), name='cart'),
]
