from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


admin.site.register(Slider)
<<<<<<< HEAD
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Trend)
admin.site.register(WishItem)
admin.site.register(Customer)
admin.site.register(Comments)
admin.site.register(Offer)
admin.site.register(Support)
admin.site.register(Seller)
admin.site.register(Payment_method)
=======
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(Trend)
# admin.site.register(WishItem)
# admin.site.register(Customer)
# admin.site.register(Comments)
# admin.site.register(Offer)
# admin.site.register(Support)
# admin.site.register(Seller)
# admin.site.register(Payment_method)
>>>>>>> 53338c0c89452d5948e18b831938bda07ac18f69



class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery

class Sub_CategoryInline(admin.TabularInline):
    fk_name = 'category'
    model = Sub_Category

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'

# @admin.register(Slider)
# class SliderAdmin(admin.ModelAdmin):
#     pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    pass

@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    pass

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    class Meta:
        model = Product
        fields = '__all__'
        inlines = [GalleryInline, Sub_CategoryInline]
class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


class Sub_CategoryInline(admin.TabularInline):
    fk_name = 'category'
    model = Sub_Category



@admin.register(Payment_method)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     form = ProductForm
#     inlines = [GalleryInline, Sub_CategoryInline]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
