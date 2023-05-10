from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import random
import string
import secrets


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200)
    image = models.ImageField(default='user_photos/img.jpg',upload_to='user_photos')
    mobile = models.CharField(max_length=10,null=True, blank=True)
    # address = models.TextField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # city = models.CharField(max_length=100, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    referral_link = models.CharField(max_length=255, unique=True, null=True, blank=True)
    referral_code = models.CharField(max_length=5, unique=True, blank=True)
    referrer_code = models.CharField(max_length=5, default='admin',blank=True)
    referral_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    registred = models.BooleanField(default=False)
    balance_hrwt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_usdt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.IntegerField(default=0, blank=False, null=False)
    wallet = models.CharField(max_length=200,null=False)
    
    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        if not self.wallet and self.user:
            self.wallet = self.user.username
    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = secrets.token_urlsafe(5)[:5]
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        letters_and_digits = string.ascii_letters + string.digits
        while True:
            referral_code = ''.join(random.choice(letters_and_digits) for _ in range(5))
            if not Customer.objects.filter(referral_link=referral_code).exists():
                return referral_code
    def get_referrals(self):
        return Customer.objects.filter(referral_by=self)

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrer', on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, related_name='invitee', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    image = models.ImageField(null=True, blank=True)
    
   
    def __str__(self):
	    return self.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
   
    def __str__(self):
	    return self.name



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=23)
    brand_name = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True )
    slug = models.SlugField(default="", null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    crown_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True)
    description = RichTextField(default="",null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    digital = models.BooleanField(default=False,null=True, blank=True)
    available = models.BooleanField(default=False,null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='user_photos', blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Gallery(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class WishItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.user)


    def get_item_price(self):
        return self.quantity * self.product.price

class Slider(models.Model):
    name = models.CharField(max_length=50, default = "", null=True)
    image = models.ImageField(upload_to='slider_img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
	    return self.name
 

class Trend(models.Model):
    product = models.ForeignKey(Product, default="", on_delete=models.CASCADE, null=True)
    number = models.PositiveIntegerField()
	
    def __str__(self):
	    return str(self.product)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=100, null=False)
	city = models.CharField(max_length=100, null=False)
	state = models.CharField(max_length=100, null=False)
	zipcode = models.CharField(max_length=100, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.order)


class Comments(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=150, null=True, blank=True)
    rate = models.IntegerField(default=1, null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.subject

class Offer(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=60, null=True)
    comment = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	    return self.subject


class Support(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=60, null=True)
    comment = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.subject


class Partnership(models.Model):
    name = models.CharField(max_length=50, null=True)
    site = models.CharField(max_length=200, null=True)

    def __str__(self):
	    return self.name


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     referral_link = models.URLField(blank=True)
#     referred_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referred')

#     def __str__(self):
#         return self.user.username

    