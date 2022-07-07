from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model


from .forms import UserChangeForm, UserCreationForm
from .models import (Category, Product, Order, Address, Customer,
                     Payment, Seller, SellerAddress, SellerBankDetail, StoreDetails)


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + \
        auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name", "parent_category"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id","name", "price", "category",
                    'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["get_product_id", "get_customer_id",
                    'product', 'quantity']

    def get_product_id(self, obj):
        return obj.id

    def get_customer_id(self, obj):
        return obj.customer.id

    def get_customer_email(self, obj):
        return obj.customer.email

    # Renames column head
    get_product_id.short_description = 'PRODUCT_ID'
    get_customer_id.short_description = 'CUSTOMER_ID'
    get_customer_email.short_description = 'EMAIL'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass

@admin.register(SellerAddress)
class SellerAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(SellerBankDetail)
class SellerBankDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(StoreDetails)
class StoreDetailsAdmin(admin.ModelAdmin):
    pass