from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import random
import string
import secrets
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.


class Referral(models.Model):
    referrer = models.ForeignKey(
        User, related_name='referrer', on_delete=models.CASCADE)
    invitee = models.ForeignKey(
        User, related_name='invitee', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer} -> {self.invitee}"


class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(
        default='user_photos/img.jpg', upload_to='user_photos')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    Course_cat = (
        ('Основные курсы', 'Основные курсы'),
        ('Занятие телом', 'Занятие телом'),
        ('Игры', 'Игры'),
    )
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(TeamMember)
    description = models.TextField(null=True)
    Category = models.CharField(
        max_length=20, choices=Course_cat, default='Основные курсы')
    order = models.PositiveIntegerField(default=0)

    def get_topics(self):
        return self.description.split('\n')

    def __str__(self):
        return self.name


class Direction(models.Model):
    name = models.CharField(max_length=100)
    sale_name = models.CharField(max_length=100, null=True)
    description = models.TextField()
    courses = models.ManyToManyField(Course)
    video_presentation = models.URLField()
    hard_skills = models.TextField()
    soft_skills = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def get_all_teachers(self):
        # Используем values() для получения словарей с данными по курсам и преподавателям
        teachers_data = self.courses.values(
            'teacher__id', 'teacher__first_name', 'teacher__last_name').distinct()

        # Преобразуем словари в объекты TeamMember
        teachers = [TeamMember(**teacher_data)
                    for teacher_data in teachers_data]

        return teachers

    def __str__(self):
        return self.name


class Customer(models.Model):

    STATUS_CHOICES = (
        ('Студент', 'Студент'),
        ('Преподаватель', 'Преподаватель'),
        ('Эксперт', 'Эксперт'),
        ('Продавец', 'Продавец'),
    )

    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200)
    image = models.ImageField(
        default='user_photos/img.jpg', upload_to='user_photos')
    mobile = models.CharField(max_length=13, null=True, blank=True)
    # address = models.TextField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # city = models.CharField(max_length=100, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    referral_link = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    referral_code = models.CharField(max_length=5, unique=True, blank=True)
    referrer_code = models.CharField(max_length=5, default='admin', blank=True)
    referral_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    registred = models.BooleanField(default=False)
    balance_tvt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    balance_usdt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    balance_hrwt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    # level = models.IntegerField(default=0, blank=False, null=False)
    wallet = models.CharField(max_length=100, default='')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Студент')
    direction = models.ForeignKey(
        Direction, null=True, blank=True, on_delete=models.SET_NULL)

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        if not self.wallet and self.user:
            self.wallet = self.user.username

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = secrets.token_urlsafe(5)[:5]
        if not self.wallet:
            self.wallet = self.user.get_username()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        letters_and_digits = string.ascii_letters + string.digits
        while True:
            referral_code = ''.join(random.choice(
                letters_and_digits) for _ in range(5))
            if not Customer.objects.filter(referral_link=referral_code).exists():
                return referral_code

    def get_referrals(self):
        return Customer.objects.filter(referral_by=self)


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        # При создании нового пользователя устанавливаем связь с направлением "Демо"
        demo_direction = Direction.objects.filter(name='Демо').first()
        if demo_direction:
            Customer.objects.create(user=instance, direction=demo_direction)


class WeaklyBoard(models.Model):
    name = models.CharField(max_length=50)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.name} - {self.course} - {self.start_time} to {self.end_time}"

class StudyGroup(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Customer)
    
    def __str__(self):
        return f"{self.direction.name} - {self.name}"


class Stream(models.Model):
    name = models.CharField(max_length=100)
    direction = models.ForeignKey(
        Direction, null=True, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    open_status = models.BooleanField(default=False)
    # ... (другие поля)

    def __str__(self):
        return f"{self.direction.name} - {self.name}"


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=500, null=True, blank=True)
    zoom_rec = models.URLField()
    homework = models.TextField()
    teachers = models.ManyToManyField(TeamMember)
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    streams = models.ForeignKey(Stream, null=True, on_delete=models.CASCADE)
    open_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VideoRec(models.Model):
    link = models.URLField()
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.link


class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=23, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)


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
    brand_name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default="", null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    crown_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(
        Sub_Category, on_delete=models.CASCADE, null=True)
    description = RichTextField(default="", null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    available = models.BooleanField(default=False, null=True, blank=True)
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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')


class WishItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_item_price(self):
        return self.quantity * self.product.price


class NewsFeed(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news_images')
    news_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class packagesCat(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Packages(models.Model):
    name = models.CharField(max_length=100)
    header = models.CharField(max_length=25)
    category = models.ForeignKey(
        packagesCat, on_delete=models.CASCADE, null=True)
    price_usd = models.CharField(max_length=25)
    price_twt = models.CharField(max_length=25)
    amount = models.PositiveBigIntegerField()
    short_desc = models.CharField(max_length=100)
    long_desc = models.CharField(max_length=500)


class Slider(models.Model):
    name = models.CharField(max_length=50, default="", null=True)
    image = models.ImageField(upload_to='slider_img')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Trend(models.Model):
    product = models.ForeignKey(
        Product, default="", on_delete=models.CASCADE, null=True)
    number = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
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
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
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
    image = models.ImageField(upload_to='partners', null=True)

    def __str__(self):
        return self.name


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     referral_link = models.URLField(blank=True)
#     referred_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referred')

#     def __str__(self):
#         return self.user.username
