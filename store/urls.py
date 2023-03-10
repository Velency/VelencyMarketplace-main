from django.urls import path
from . import views

urlpatterns = [
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
    path('offers/', views.offers, name="offers"),
    #support 
    path('support/', views.support, name="support"),
    #tariffs
    path('tariffs/', views.tariffs, name="tariffs"),
    #politic
    path('politic/', views.politic, name="politic"),
 
    #main pages
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    #seller reg
    path('create_seller', views.create_seller, name="create_seller"),

]