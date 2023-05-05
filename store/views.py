
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.dispatch import receiver
from django.db.models.signals import post_save


from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UpdateCustomerForm, CommentsForm, SupportForm,CustomerForm,CustomerOfferForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .s3 import upload_to_s3, download_from_s3
from velencystore.settings import RECIPIENTS_EMAIL, EMAIL_HOST_USER


# Create your views here.

#mail
from django.core.mail import send_mail
from .forms import FeedbackForm

# metamask
from web3 import Web3
from moralis import *
import requests
from django.contrib.auth.models import User

API_KEY = 'cP2QKvv4ccJNAjffgnL5rnRjq0rjTf6iRXFm3odaHxbrzAsnOOXG5ggVYEEu4XfL'
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit


def moralis_auth(request):
    return render(request, 'login.html', {})

def my_profile(request):
     if request.user.customer.registred:
        return render(request, 'store/profile.html', {})
     else:
        return redirect('account')

def request_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": "2024-01-01T00:00:00.000Z",
      "notBefore": "2023-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))


def verify_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)

    user = None  # assign a default value to user

    if x.status_code == 201:
        # user can authenticate
        eth_address = json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # create a new customer instance with the user
            customer_data = {'user': user,'wallet': eth_address}
            if 'first_name' in data:
                customer_data['first_name'] = data['first_name']
            else:
                customer_data['first_name'] = 'New user'
            customer = Customer.objects.create(**customer_data)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                request.session['user_id'] = user.id  # сохраняем id пользователя в сессию
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))


# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         customer_name = "New user {}".format(instance.id)
#         Customer.objects.create(user=instance, name=customer_name)


def LoginPage(request):
    # create a new Moralis instance with the application ID and server URL
    moralis = Moralis(
        application_id='cP2QKvv4ccJNAjffgnL5rnRjq0rjTf6iRXFm3odaHxbrzAsnOOXG5ggVYEEu4XfL',
        server_url='https://your_moralis_server_url/api',
    )

    # create a new Web3 instance using the user's browser provider
    web3 = Web3(Web3.WebsocketProvider(moralis.get_web3_socket()))

    # initiate the Metamask authentication process
    login_data = moralis.authenticate(web3)

    # redirect the user to the authentication URL
    return redirect('profile')

def index(request):
    return render(request, 'store/index.html')

# def packet_buy(request):
#     data = cartData(request)
    
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']
#     partners = Partnership.objects.all()
#     context = {'partners':partners, 'items':items, 'order':order, 'cartItems':cartItems, }
#     return render(request, 'store/packet_buy.html', context)

# Viwe.py 


def packet_buy(request):
    result = None
    total = None
    product= None
    value = request.GET.get('value')
    if value == '50':
        result = '50'
        total = '150'
        product = 'Packet 50 USDT'
    elif value == '100':
        result = '100'
        total = '300'
        product = 'Packet 100 USDT'
    elif value == '250':
        result = '250'
        total = '750'
        product = 'Packet 250 USDT'
    elif value == '500':
        result = '500'
        total = '1500'
        product = 'Packet 500 USDT'
    elif value == '1000':
        result = '1000'
        total = '3000'
        product = 'Packet 1000 USDT'
    elif value == '2500':
        result = '2500'
        total = '7500'
        product = 'Packet 2500 USDT'
    elif value == '5000':
        result = '5000'
        total = '15000'
        product = 'Packet 5000 USDT'
    elif value == '10000':
        result = '10000'
        total = '30000'
        product = 'Packet 10000 USDT'
    
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                send_mail(
                    'Сообщение из формы обратной связи',
                    f'От: {name}\nEmail: {email}\n\n{message}\nПриобретен продукт:{product} \n by: {request.user.customer.name} ',
                     EMAIL_HOST_USER, [RECIPIENTS_EMAIL,'hrworld42@gmail.com','fidanur23@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'Ошибка отправки сообщения! {e}')
                
            else:
                messages.success(request, 'Сообщение успешно отправлено.')
                form = FeedbackForm()
                
        else:
            print(form.errors)
            messages.error(request, 'Ошибка формы!')
            
    return render(request, 'store/packet_buy.html', {'form': form, 'result': result, 'total': total, 'product': product})




    # if request.method == 'POST':
    #     # если метод POST, проверим форму и отправим письмо
    #     form = FeedbackForm(request.POST)
    #     if form.is_valid():
    #         subject = form.cleaned_data['subject']
    #         from_email = form.cleaned_data['from_email']
    #         message = form.cleaned_data['message']
    #         try:
    #             send_mail(f'{subject} от {from_email}', message,
    #                       EMAIL_HOST_USER, RECIPIENTS_EMAIL)
    #         except Exception as e:
    #             messages.error(request, f'Ошибка отправки сообщения! {e}')
    #         else:
    #             messages.success(request, 'Сообщение успешно отправлено.')
    #             form = FeedbackForm()
    # else:
    #     return HttpResponse('Неверный запрос.')




    return render(request, 'store/packet_buy.html', {'form': form, 'product': product})


  # End View.py




def store(request):
    
    products = Product.objects.filter(available=True)
    sliders = Slider.objects.all()

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()

    trends = Trend.objects.order_by('-number')[0:30]
    
    categoryID = request.GET.get('category')
    partners = Partnership.objects.all()
    if categoryID:
        products = Product.objects.filter(sub_category = categoryID)
    else:
        products = Product.objects.filter(available=True)

    params={ 'partners':partners, 'categories':categories, 'products':products, 'trends':trends,  'cartItems':cartItems, 'sliders':sliders,  'order':order, 'items':items }

    return render(request, 'store/store.html', params)


def wishlist(request):
    wish_items = WishItem.objects.filter(user=request.user)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context={'partners':partners, 'wish_items':wish_items, 'data':data, 'cartItems':cartItems, 'order':order, 'items':items, 'categories':categories}
    return render(request, 'store/wishlist.html', context)


def addToWishlist(request):
    if request.method =="POST":
        product_id = request.POST.get('product-id')
        product = Product.objects.get(id=product_id)

        try:
            wish_item = WishItem.objects.get(user=request.user, product=product)
            if wish_item:
                wish_item.quantity += 1
                wish_item.save()
        except:
            WishItem.objects.create(user=request.user, product=product)
        finally:
            return HttpResponseRedirect(reverse('wishlist'))


def DeleteFormWishList(request):
    if request.method == "POST":
        item_id = request.POST.get('item-id')
        WishItem.objects.filter(id=item_id).delete()
        return HttpResponseRedirect(reverse('wishlist'))

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
def account(request):
    if request.method == "POST":
        customer = request.user.customer
        form = UpdateCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            # Save the uploaded image to the default storage
            image_file = form.cleaned_data.get('image')
            if image_file:
                filename = default_storage.save(image_file.name, ContentFile(image_file.read()))
                customer.image = filename

            customer.registred = True
            # Get the referrer code entered by the customer
            referrer_code = form.cleaned_data.get('referrer_code')
            if referrer_code:
                # Find the customer who has the entered referral code as their referral_code
                referrer = Customer.objects.filter(referral_code=referrer_code).first()
                if referrer:
                    # Add the referral to the database
                    Referral.objects.create(referrer=request.user, invitee=referrer.user)
                    # Set the referral_by field of the current customer to the referrer
                    customer.referral_by = referrer

            form.save()
            messages.success(request, 'Profile was updated')
            return redirect('my_profile')
    else:
        form = UpdateCustomerForm(instance=request.user.customer)

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'cartItems': cartItems, 'form': form, 'order': order, 'items': items, 'categories': categories}
    return render(request, 'store/customer_form.html', context)






def orders(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    uid = request.session.get('_auth_user_id')
    customer = Customer.objects.get(pk=uid)
    orders = Order.objects.filter(customer=customer)
    print(customer, orders)

    context={'partners':partners, 'categories':categories, 'cartItems':cartItems, 'items':items, 'order':order, 'orders':orders}
    return render(request, 'store/my_orders.html', context)


def product_details(request,id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product = Product.objects.filter(id=id).first()
    images = Gallery.objects.filter(product=product)
    categories =Category.objects.all()
    reviews = Comments.objects.filter(product=product)
    partners = Partnership.objects.all()
    context = {'partners':partners, 'product':product, 'reviews':reviews, 'images':images, 'categories':categories, 'cartItems':cartItems, 'order':order, 'items':items }
    return render(request, 'store/product-details.html', context)


def addComment(request, id):
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            data = Comments()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_customer = request.user.customer
            data.customer_id = current_customer.id
            data.save()
            return HttpResponseRedirect('.')


def support(request):
    form = SupportForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            data = Support()
            data.subject = form.cleaned_data['subject']
            data.email = form.cleaned_data['email']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            current_customer = request.user.customer
            data.customer_id = current_customer.id
            data.save()
            return HttpResponseRedirect ('.')
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context = { 'partners':partners, 'cartItems':cartItems, 'categories':categories, 'order':order, 'items':items, 'form':form, }
    return render(request, 'store/support.html', context)


def trends(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    trends = Trend.objects.all()

    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners':partners, 'cartItems':cartItems, 'categories':categories, 'order':order, 'items':items, 'trends':trends}
    return render(request, 'store/trend-list.html', context)


def offers(request):
    form = CustomerOfferForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            data = Offer()
            data.subject = form.cleaned_data['subject']
            data.email = form.cleaned_data['email']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            current_customer = request.user.customer
            data.customer_id = current_customer.id
            data.save()
            return HttpResponseRedirect('.')
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context ={'partners':partners, 'form':form,  'cartItems':cartItems, 'categories':categories, 'order':order, 'items':items }
    return render(request, 'store/customers_offers.html', context)



def all_product_list(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    partners = Partnership.objects.all()
    products = Product.objects.filter(available=True).order_by('-id')
    context = {'partners':partners, 'cartItems':cartItems, 'order': order, 'items':items, 'products':products  }
    return render(request, 'store/all_products.html', context)


def sub_view_all(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    categoryID = request.GET.get('category')
    partners = Partnership.objects.all()
    if categoryID:
        product = Product.objects.filter(sub_category = categoryID)
    else:
        product = Product.objects.filter(available=True)
    
    context = {'partners':partners, 'cartItems':cartItems, 'categories':categories, 'product':product,  'order': order, 'items':items,  'data':data  }
    return render(request, 'store/sub_view_all.html', context)




def view_all(request, category_id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    category = Category.objects.get(id=category_id)
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    data = Product.objects.filter( category=category,  available=True).order_by('-id')
    
    context = {'partners':partners, 'cartItems':cartItems,  'categories':categories, 'order': order, 'items':items, 'category':category, 'data':data  }
    return render(request, 'store/view_all.html', context)



def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners':partners,'items':items, 'order':order, 'categories':categories, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    partners = Partnership.objects.all()
    context = {'partners':partners, 'items':items, 'order':order, 'cartItems':cartItems, }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else: 
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST) 
        if form.is_valid(): 
        #saving the registered user
            user = form.save()
            username= form.cleaned_data.get('username')
        #create customer
            Customer.objects.create(user=user, name=username, email=user.email)
            messages.success(request, 'Account was created for' + username)
            return redirect('loginPage')
        
    
        context = {'form':form}
        return render(request, 'store/reg.html', context)



def search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    query = request.GET.get('query')
    print(query)
    product = Product.objects.filter(name__icontains = query)
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    
    params ={'partners':partners, 'cartItems':cartItems, 'order':order, 'categories':categories, 'items':items, 'product':product}
    return render(request, 'store/search.html', params)


def tariffs (request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories =Category.objects.all()
    partners = Partnership.objects.all()
    context = {  'cartItems':cartItems, 'order':order, 'items':items, 'categories':categories, 'partners':partners}
    return render(request, 'store/packages.html', context)

def politic (request):
    return render(request, 'store/politic.html')


def registerCustomer(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            # Создаем пользователя
            user = user_form.save()
            # Создаем объект Customer связанный с пользователем
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            # Аутентификация пользователя и перенаправление на главную страницу
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        user_form = UserCreationForm()
        customer_form = CustomerForm()
    return render(request, 'create_customer.html', {'user_form': user_form, 'customer_form': customer_form})

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('profile')
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

@login_required
def referral_list(request):
    referrals = Referral.objects.filter(referrer=request.user)
    return render(request, 'referral_list.html', {'referrals': referrals})




# @login_required
# def referral(request):
#     user = request.user
#     if user.userprofile.referred_by:
#         referred_by = user.userprofile.referred_by.username
#     else:
#         referred_by = None
#     referral_link = request.build_absolute_uri('/register/') + '?ref=' + user.username
#     user.userprofile.referral_link = referral_link
#     user.userprofile.save()
#     return render(request, 'profile.html', {'referral_link': referral_link, 'referred_by': referred_by})