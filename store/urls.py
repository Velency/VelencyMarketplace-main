from django.urls import path, include
from . import views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #log/reg pages
    path('login/', views.loginPage, name="loginPage"),
    path('accounts/login/',views.loginPage, name="loginPage"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logoutUser"),
    #product pages
    path('product-list/<int:category_id>', views.view_all, name="product-list"),
    path('sub-product-list/', views.sub_view_all, name="sub-product-list"),
    path('trends-list/', views.trends, name="trends-list"),
    path('all-product-list/', views.all_product_list, name="all-product-list"),
    #customer details
    path('profile/', views.account, name="profile"),
    path('orders/', views.orders, name="orders"),
    #searsh
    path('search/', views.search, name="search"),
    #product details
    path('product/<str:id>', views.product_details, name="product-details"),
    #comments
    path('addcomment/<int:id>', views.addComment, name="addcomment"),
    #wishlist
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add-to-wishlist/', views.addToWishlist, name="add-to-wishlist"),
    path('delete-from-wishlist/', views.DeleteFormWishList, name="delete-from-wishlist"),
    #suggestions
    # path('offers/', views.offers, name="offers"),
    #support 
    path('support/', views.support, name="support"),
    #tariffs
    path('tariffs/', views.tariffs, name="tariffs"),
    #politic
    path('politic/', views.politic, name="politic"),
 
    #main pages
    path('', views.index, name="index"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('packet_buy/', views.packet_buy, name="packet_buy"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    #seller reg
    # path('seller_dashboard/', views.seller_dashboard, name="seller_dashboard"),
    # path('create_seller/', views.create_seller, name="create_seller"),
    # path('create_product/',views.create_product, name="create_product" ),
    #moralis reg
    path('moralis_auth', views.moralis_auth, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('verify_message', views.verify_message, name='verify_message'),
    


]