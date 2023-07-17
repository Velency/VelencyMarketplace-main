
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Customer
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.db.models.signals import post_save

from django.contrib.auth.forms import UserCreationForm
from .forms import UpdateCustomerForm, CommentsForm, SupportForm, CustomerOfferForm, WalletForm, WithdrawForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from velencystore.settings import RECIPIENTS_EMAIL, EMAIL_HOST_USER
from django.utils import timezone
# Create your views here.

# mail
from django.core.mail import send_mail
from .forms import FeedbackForm

# metamask
from web3 import Web3
# from moralis import *
import requests
from django.contrib.auth.models import User


API_KEY = 'cP2QKvv4ccJNAjffgnL5rnRjq0rjTf6iRXFm3odaHxbrzAsnOOXG5ggVYEEu4XfL'
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit


# ГЛАВНАЯ Страница
def index(request):
    news_feed = NewsFeed.objects.all()
    team_members = TeamMember.objects.all()
    item_count = news_feed.count()
    # partners = Partnership.objects.all()
    context = {'news_feed': news_feed, 'item_count': item_count,
               'team_members': team_members, }
    return render(request, 'store/index.html', context)


def store(request):

    products = Product.objects.filter(available=True)
    sliders = Slider.objects.all()

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()

    trends = Trend.objects.order_by('-number')[0:30]

    categoryID = request.GET.get('category')
    partners = Partnership.objects.all()
    if categoryID:
        products = Product.objects.filter(sub_category=categoryID)
    else:
        products = Product.objects.filter(available=True)

    params = {'partners': partners, 'categories': categories, 'products': products,
              'trends': trends,  'cartItems': cartItems, 'sliders': sliders,  'order': order, 'items': items}

    return render(request, 'store/store.html', params)


# Авторизация и регистрация


def authenticate_wallet(request):
    data = json.loads(request.body)
    address = data.get('address')

    # Check if the user already exists
    try:
        user = User.objects.get(username=address)
    except User.DoesNotExist:
        # Create a new user account
        user = User.objects.create_user(username=address)

    # Create a Customer object associated with the user
    customer, created = Customer.objects.get_or_create(user=user)
    customer.name = data.get('name', '')
    customer.first_name = data.get('first_name', '')
    customer.last_name = data.get('last_name', '')
    customer.email = data.get('email', '')
    customer.mobile = data.get('mobile', '')
    # Save the Customer object
    customer.save()

    # Log in the user
    login(request, user)

    return JsonResponse({'success': True})


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
            customer_data = {'user': user, 'wallet': eth_address}
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
                # сохраняем id пользователя в сессию
                request.session['user_id'] = user.id
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))


def logoutUser(request):
    logout(request)
    return redirect('index')

# Работа с аккаунтами


@login_required
def my_profile(request):
    if request.user.customer:
        return render(request, 'store/profile.html', {})
    else:
        return redirect('customer_form')


@login_required
def send_email(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Create a new Withdraw model instance
            withdraw = Withdraw.objects.create(
                amount=amount,
                date=timezone.now().date(),
                user=request.user,
                status='open'
            )

            try:
                send_mail(
                    'Запрос на вывод средств',
                    f'От: {request.user.customer.first_name} {request.user.customer.last_name}\nEmail: {request.user.customer.email}\n\nАдрес кошелька: {request.user.customer.wallet}\nСумма вывода:{amount}\n\nБаланс\nTWT: {request.user.customer.balance_tvt}\nUSDT: {request.user.customer.balance_usdt}\nHRWT: {request.user.customer.balance_hrwt} \n by: {request.user.customer.name} ',
                    EMAIL_HOST_USER, [RECIPIENTS_EMAIL, 'fidanur23@gmail.com'],
                    fail_silently=False,
                )

                return JsonResponse({'message': 'Письмо успешно отправлено'})
            except Exception as e:
                return JsonResponse({'error': f'Ошибка отправки письма: {e}'}, status=500)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': 'Неверные данные формы', 'errors': form.errors}, status=400)


def account(request):
    form = None  # установить значение по умолчанию
    wallet_form = None  # установить значение по умолчанию
    if request.method == "POST":
        customer = request.user.customer
        form = UpdateCustomerForm(
            request.POST, request.FILES, instance=customer)
        wallet_form = WalletForm(request.POST, instance=customer)
        if form.is_valid():
            customer.registred = True
            # Get the referrer code entered by the customer
            referrer_code = form.cleaned_data.get('referrer_code')
            if referrer_code:
                # Find the customer who has the entered referral code as their referral_code
                referrer = Customer.objects.filter(
                    referral_code=referrer_code).first()
                if referrer:
                    # Add the referral to the database
                    Referral.objects.create(
                        referrer=request.user, invitee=referrer.user)
                    # Set the referral_by field of the current customer to the referrer
                    customer.referral_by = referrer

            form.save()
            messages.success(request, 'Profile was updated')
            return redirect('my_profile')
        if wallet_form.is_valid():
            wallet_form.save()
            messages.success(request, 'Wallet was updated')
            return redirect('my_profile')
    else:
        form = UpdateCustomerForm(instance=request.user.customer)
        wallet_form = WalletForm(instance=request.user.customer)
    return render(request, 'store/customer_form.html', {'form': form, 'wallet_form': wallet_form})


# Viwe.py

# Пакеты криптовалют и токена
@login_required
def tariffs(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()

    # Получаем все пакеты из модели Packages
    packages = Packages.objects.all()

    context = {
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'categories': categories,
        'partners': partners,
        'packages': packages,
    }
    return render(request, 'store/packages.html', context)


@login_required
def packet_buy(request):
    package_id = request.GET.get('package')
    try:
        package = Packages.objects.get(id=package_id)
    except Packages.DoesNotExist:
        package = None

    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = request.user.customer.name
            email = request.user.customer.email
            message = form.cleaned_data['message']

            try:
                send_mail(
                    'Сообщение из формы обратной связи',
                    f'От: {name}\nEmail: {email}\n\n{message}\nПриобретен продукт: {package["header"]} \nby: {request.user.customer.name} ',
                    EMAIL_HOST_USER, [
                        RECIPIENTS_EMAIL, 'fidanur23@gmail.com', 'f.usmanov@hrworld.live'],
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

    context = {
        'result': package.price_twt if package else '',
        'total': package.price_usd if package else '',
        'package_description': package.long_desc if package else '',
    }
    return render(request, 'store/payment.html', context)


# Walletconnect


# Модули маркетплейса
@login_required
def wishlist(request):
    wish_items = WishItem.objects.filter(user=request.user)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'wish_items': wish_items, 'data': data,
               'cartItems': cartItems, 'order': order, 'items': items, 'categories': categories}
    return render(request, 'store/wishlist.html', context)


@login_required
def addToWishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product-id')
        product = Product.objects.get(id=product_id)

        try:
            wish_item = WishItem.objects.get(
                user=request.user, product=product)
            if wish_item:
                wish_item.quantity += 1
                wish_item.save()
        except:
            WishItem.objects.create(user=request.user, product=product)
        finally:
            return HttpResponseRedirect(reverse('wishlist'))


@login_required
def DeleteFormWishList(request):
    if request.method == "POST":
        item_id = request.POST.get('item-id')
        WishItem.objects.filter(id=item_id).delete()
        return HttpResponseRedirect(reverse('wishlist'))


@login_required
def orders(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    uid = request.session.get('_auth_user_id')
    customer = Customer.objects.get(pk=uid)
    orders = Order.objects.filter(customer=customer)
    print(customer, orders)

    context = {'partners': partners, 'categories': categories,
               'cartItems': cartItems, 'items': items, 'order': order, 'orders': orders}
    return render(request, 'store/my_orders.html', context)


def product_details(request, id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product = Product.objects.filter(id=id).first()
    images = Gallery.objects.filter(product=product)
    categories = Category.objects.all()
    reviews = Comments.objects.filter(product=product)
    partners = Partnership.objects.all()
    context = {'partners': partners, 'product': product, 'reviews': reviews, 'images': images,
               'categories': categories, 'cartItems': cartItems, 'order': order, 'items': items}
    return render(request, 'store/product-details.html', context)


@login_required
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
            product_url = reverse('product', args=[id])
            return HttpResponseRedirect(product_url)
    else:
        product_url = reverse('product-details', args=[id])
        return HttpResponseRedirect(product_url)


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
            return HttpResponseRedirect('.')
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'cartItems': cartItems,
               'categories': categories, 'order': order, 'items': items, 'form': form, }
    return render(request, 'store/support.html', context)


def trends(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    trends = Trend.objects.all()

    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'cartItems': cartItems,
               'categories': categories, 'order': order, 'items': items, 'trends': trends}
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
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'form': form,  'cartItems': cartItems,
               'categories': categories, 'order': order, 'items': items}
    return render(request, 'store/customers_offers.html', context)


def all_product_list(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    partners = Partnership.objects.all()
    products = Product.objects.filter(available=True).order_by('-id')
    context = {'partners': partners, 'cartItems': cartItems,
               'order': order, 'items': items, 'products': products}
    return render(request, 'store/all_products.html', context)


def sub_view_all(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    partners = Partnership.objects.all()
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID)
    else:
        product = Product.objects.filter(available=True)

    context = {'partners': partners, 'cartItems': cartItems, 'categories': categories,
               'product': product,  'order': order, 'items': items,  'data': data}
    return render(request, 'store/sub_view_all.html', context)


def view_all(request, category_id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    category = Category.objects.get(id=category_id)
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    data = Product.objects.filter(
        category=category,  available=True).order_by('-id')

    context = {'partners': partners, 'cartItems': cartItems,  'categories': categories,
               'order': order, 'items': items, 'category': category, 'data': data}
    return render(request, 'store/view_all.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
    partners = Partnership.objects.all()
    context = {'partners': partners, 'items': items, 'order': order,
               'categories': categories, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    partners = Partnership.objects.all()
    context = {'partners': partners, 'items': items,
               'order': order, 'cartItems': cartItems, }
    return render(request, 'store/checkout.html', context)


@login_required
def updateItem(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
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


def search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    query = request.GET.get('query')
    print(query)
    product = Product.objects.filter(name__icontains=query)
    categories = Category.objects.all()
    partners = Partnership.objects.all()

    params = {'partners': partners, 'cartItems': cartItems, 'order': order,
              'categories': categories, 'items': items, 'product': product}
    return render(request, 'store/search.html', params)


def politic(request):
    return render(request, 'store/politic.html')


@login_required
def referral_list(request):
    referrals = Referral.objects.filter(referrer=request.user)
    return render(request, 'referral_list.html', {'referrals': referrals})


# Блок с Преподавателями

def trainers(request):
    return render(request, 'store/trainers.html')


def schedule(request):
    return render(request, 'store/schedule.html')


def tasks(request):
    return render(request, 'store/tasks.html')
