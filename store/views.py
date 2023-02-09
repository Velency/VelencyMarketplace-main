
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder




from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerOfferForm, UpdateCustomerForm, CommentsForm, SupportForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from .s3 import upload_to_s3, download_from_s3


# Create your views here.










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



def account(request):
	if request.method =="POST":
		customer = request.user.customer
		form = UpdateCustomerForm(request.POST, request.FILES, instance = customer)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile was updated')
			return redirect('profile')
	else:
		form = UpdateCustomerForm(instance=request.user.customer)
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	categories =Category.objects.all()
	partners = Partnership.objects.all()
	context ={'partners':partners, 'cartItems':cartItems,  'form':form, 'order':order, 'items':items,  'categories':categories}
	return render(request, 'store/customerDetail.html', context)


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
			return HttpResponseRedirect('/')


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
	return redirect('loginPage')


def register(request):
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
	context = {'cartItems':cartItems, 'order':order, 'items':items, 'categories':categories, 'partners':partners}
	return render(request, 'store/tariffs.html', context)

def politic (request):
	return render(request, 'store/politic.html')