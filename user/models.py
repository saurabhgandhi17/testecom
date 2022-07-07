from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import models


'''
AbstractUser user model
'''
class User(AbstractUser):
    name = models.CharField(_("Name"), blank=False, max_length=255)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


'''
Model to store customer info
'''
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="customer")
    def __str__(self):
        return self.user.username


'''
Model to store customer address
'''
class Address(models.Model):
    address_line1 = models.CharField(_("Address 1"), blank=False, max_length=255)
    address_line2 = models.CharField(_("Address 2"), blank=False, max_length=255)
    mobile_number = models.IntegerField(_('Mobile Number'),blank=False)
    city = models.CharField(_("city"), blank=False, max_length=255,default="")
    state = models.CharField(_("state"), blank=False, max_length=255,default="")
    pincode = models.CharField(_('Area pincode'),blank=False,max_length=30)
    customer = models.ForeignKey(User, related_name="customer_address" ,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return str(self.id)


'''
Model to store customer payment details
'''
class Payment(models.Model):
    account_number =  models.CharField(_("Account number"), blank=True, max_length=255)
    account_holder_name =  models.CharField(_("Account holder name"), blank=True, max_length=255)
    expiry_date =  models.DateField(_("expiry date"), blank=True, max_length=255)
    customer = models.ForeignKey(User, related_name="payments" ,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return str(self.id)


'''
Model to store seller info
'''
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="sellers")
    mobile_number = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"

    def __str__(self):
        return self.user.username


class SellerAddress(models.Model):
    address_line1 = models.CharField(_("Address 1"), blank=False, max_length=255)
    address_line2 = models.CharField(_("Address 2"), blank=False, max_length=255)
    city = models.CharField(_("city"), blank=False, max_length=255,default="")
    state = models.CharField(_("state"), blank=False, max_length=255,default="")
    pincode = models.CharField(_('Area pincode'),blank=False,max_length=30)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,  related_name="seller_address")

    class Meta:
        verbose_name = "seller_address"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.seller.user.username


class SellerBankDetail(models.Model):
    bank_name = models.CharField(_('Bank Name'),blank=False,max_length=30)
    city = models.CharField(_('City'),blank=False,max_length=30)
    state = models.CharField(_('State'),blank=False,max_length=30)
    branch = models.CharField(_('Branch'),blank=False,max_length=30)
    business_type = models.CharField(_('Business type'),blank=False,max_length=30)
    PAN = models.CharField(_('PAN'),blank=False,max_length=30)
    address_proof =  models.CharField(_('Address proof'),blank=False,max_length=30)
    cancel_cheque = models.CharField(_('cancel cheque'),blank=False,max_length=30)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,  related_name="seller_bank_details")

    class Meta:
        verbose_name = "seller_bankdetail"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.seller.user.username


class StoreDetails(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,  related_name="stores")
    name = models.CharField(_('Area pincode'),blank=False,max_length=30)
    description=models.CharField(_('Area pincode'),blank=False,max_length=30)
    logo = models.CharField(_('Area pincode'),blank=False,max_length=30)
    GSTIN = models.CharField(max_length=32)
    TAN = models.CharField(max_length=32)
    mobile_number = models.IntegerField()

    class Meta:
        verbose_name = "seller_store_detail"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.seller.user.username

'''
Model use to store the category name
'''
class Category(models.Model):
    # self filed to make category-subcategory
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subcategory', blank=True, null=True)
    name = models.CharField(_("Name"), blank=False, max_length=255)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


'''
Model to store product details
'''
class Product(models.Model):
    name = models.CharField(_("Name"), blank=False, max_length=255)
    price = models.IntegerField(_("Price"), default=0)
    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=1250, default='', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


'''
Model to store order details
'''
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
   

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
