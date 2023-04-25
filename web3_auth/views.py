import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# API_KEY = 'cP2QKvv4ccJNAjffgnL5rnRjq0rjTf6iRXFm3odaHxbrzAsnOOXG5ggVYEEu4XfL'
# if API_KEY == 'WEB3_API_KEY_HERE':
#     print("API key is not set")
#     raise SystemExit
# def moralis_auth(request):
#     return render(request, 'login.html', {})

# def my_profile(request):
#     return render(request, 'profile.html', {})

# def request_message(request):
#     data = json.loads(request.body)
#     print(data)

#     REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
#     request_object = {
#       "domain": "defi.finance",
#       "chainId": 1,
#       "address": data['address'],
#       "statement": "Please confirm",
#       "uri": "https://defi.finance/",
#       "expirationTime": "2024-01-01T00:00:00.000Z",
#       "notBefore": "2023-01-01T00:00:00.000Z",
#       "timeout": 15
#     }
#     x = requests.post(
#         REQUEST_URL,
#         json=request_object,
#         headers={'X-API-KEY': API_KEY})

#     return JsonResponse(json.loads(x.text))


# def verify_message(request):
#     data = json.loads(request.body)
#     print(data)

#     REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
#     x = requests.post(
#         REQUEST_URL,
#         json=data,
#         headers={'X-API-KEY': API_KEY})
#     print(json.loads(x.text))
#     print(x.status_code)

#     user = None  # assign a default value to user

#     if x.status_code == 201:
#         # user can authenticate
#         eth_address=json.loads(x.text).get('address')
#         print("eth address", eth_address)
#         try:
#             user = User.objects.get(username=eth_address)
#         except User.DoesNotExist:
#             user = User(username=eth_address)
#             user.is_staff = False
#             user.is_superuser = False
#             user.save()

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 request.session['auth_info'] = data
#                 request.session['verified_data'] = json.loads(x.text)
#                 return JsonResponse({'user': user.username})
#             else:
#                 return JsonResponse({'error': 'account disabled'})
#     else:
#         return JsonResponse(json.loads(x.text))
        
#     # assign a value to user outside the if statement, if needed
#         Customer.objects.create(user=user)

# @login_required
# def create_customer(request):
#     user = request.user
#     try:
#         customer = Customer.objects.get(user=user)
#     except Customer.DoesNotExist:
#         # create a new customer object for the user
#         customer = Customer.objects.create(user=user, email=user.email)
        
#     if request.method == 'POST':
#         # get form data and update customer object
#         customer.name = request.POST.get('name')
#         customer.email = request.POST.get('email')
#         customer.image = request.FILES.get('image')
#         customer.mobile = request.POST.get('mobile')
#         customer.address = request.POST.get('address')
#         customer.country = request.POST.get('country')
#         customer.city = request.POST.get('city')
#         customer.state = request.POST.get('state')
#         customer.zipcode = request.POST.get('zipcode')
#         customer.save()
#         return redirect('store')

#     return render(request, 'create_customer.html', {'customer': customer})